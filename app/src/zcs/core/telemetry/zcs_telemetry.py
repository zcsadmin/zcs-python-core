import base64
import logging
import threading

from typing import Any

from zcs.core.settings.telemetry_settings import TelemetrySettings, telemetry_settings


class ZcsTelemetry:

    def __init__(
        self,
        telemetry_settings: TelemetrySettings = telemetry_settings,
        logger: logging.Logger | None = None,
        service_name: str | None = "zcs-app",
        service_version: str | None = "0.0.0",
        service_environment: str | None = "undefined",
    ) -> None:
        self._telemetry_initialized = False
        self._telemetry_lock = threading.Lock()
        self._telemetry_settings = telemetry_settings
        self._logger = logger or logging.getLogger(__name__)
        self._service_name = service_name
        self._service_version = service_version
        self._service_environment = service_environment
        self._meter = None
        self._meters = {}
        self._tracer = None
        self._instrumented_apps = set()
        self._custom_metrics = {}
        self._prometheus_counters = {}
        self._alloy_metrics_via_prometheus = False

        self._initialize_telemetry()

    def instrument_fastapi_app(self, fastapi_app) -> None:

        if not self._telemetry_initialized:
            return

        try:
            from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
            from prometheus_fastapi_instrumentator import Instrumentator, metrics
        except ImportError:
            self._logger.warning("FastAPI OpenTelemetry instrumentation is not installed.")
            return

        app_id = id(fastapi_app)
        if app_id in self._instrumented_apps:
            return

        FastAPIInstrumentor.instrument_app(fastapi_app)
        self._instrumented_apps.add(app_id)
        self._fastapi_metrics = metrics

        Instrumentator().instrument(fastapi_app).expose(fastapi_app)

    def get_meter(self):
        if not self._telemetry_initialized:
            self._logger.warning("Telemetry is not initialized - returning None for meter")
            return None
        return self._meter

    def get_tracer(self):
        if not self._telemetry_initialized:
            self._logger.warning("Telemetry is not initialized - returning None for tracer")
            return None
        return self._tracer

    def is_telemetry_enabled(self) -> bool:
        return self._telemetry_initialized

    def counter_create(self, name, unit, description):
        if not self._telemetry_initialized:
            self._logger.warning("Telemetry is not initialized - cannot create counter")
            return

        if not self._meters and not self._alloy_metrics_via_prometheus:
            self._logger.warning("No telemetry meters are initialized - cannot create counter")
            return

        counters = {}
        for meter_key, meter in self._meters.items():
            counters[meter_key] = meter.create_counter(name=name, unit=unit, description=description)
        self._custom_metrics[name] = counters

        if self._alloy_metrics_via_prometheus:
            try:
                from prometheus_client import Counter as PrometheusCounter
                safe_name = name.replace(".", "_").replace("-", "_")
                self._prometheus_counters[name] = PrometheusCounter(safe_name, description)
            except ImportError:
                self._logger.warning("prometheus_client is not installed - Alloy Prometheus counter skipped")

    def counter_add(self, name, data=None):
        if not self._telemetry_initialized:
            self._logger.warning("Telemetry is not initialized - cannot add to counter")
            return

        amount = 1
        attributes = {}
        if isinstance(data, dict):
            if "value" in data and isinstance(data["value"], (int, float)):
                amount = data["value"]
                attributes = {k: v for k, v in data.items() if k != "value"}
            else:
                attributes = data

        counters = self._custom_metrics.get(name)
        if counters:
            for counter in counters.values():
                counter.add(amount, attributes)
        elif not self._prometheus_counters.get(name):
            self._logger.warning("Counter '%s' is not initialized", name)
            return

        prometheus_counter = self._prometheus_counters.get(name)
        if prometheus_counter is not None:
            if attributes:
                prometheus_counter.labels(**attributes).inc(amount)
            else:
                prometheus_counter.inc(amount)

    def _initialize_telemetry(self) -> None:

        # Initialization is idempotent - only the first call will set up telemetry, subsequent calls will be no-ops
        if self._telemetry_initialized:
            return

        # OTLP configuration is required for telemetry to be enabled - if not present, skip initialization
        if not self._telemetry_settings.has_otlp_config and not self._telemetry_settings.has_alloy_config:
            self._logger.warning("Neither OTLP nor Alloy configuration found - telemetry initialization skipped")
            return

        # Import OpenTelemetry modules here to avoid hard dependency
        modules = self._import_telemetry_modules()
        if modules is None:
            return

        # Use a lock to ensure that only one thread can initialize telemetry at a time in case of concurrent calls
        with self._telemetry_lock:
            resource = self._build_resource()

            telemetry_connections_initialized = False
            tracer_provider = None
            tracer_provider_registered = False

            if self._telemetry_settings.has_otlp_config:
                auth_header = self._build_basic_auth_header()

                metric_endpoint = f"{self._telemetry_settings.grafana_otlp_url}/v1/metrics"
                metric_exporter = modules["OTLPMetricExporter"](
                    endpoint=metric_endpoint,
                    headers={"Authorization": auth_header},
                )
                metric_reader = modules["PeriodicExportingMetricReader"](
                    metric_exporter,
                    export_interval_millis=self._telemetry_settings.metrics_export_interval_millis,
                )
                meter_provider = modules["MeterProvider"](resource=resource, metric_readers=[metric_reader])
                modules["metrics"].set_meter_provider(meter_provider)
                otlp_meter = meter_provider.get_meter(self._service_name, self._service_version)
                self._meters["otlp"] = otlp_meter
                if self._meter is None:
                    self._meter = otlp_meter
                telemetry_connections_initialized = True
                self._logger.info("OTLP metrics exporter enabled: %s", metric_endpoint)

                trace_endpoint = f"{self._telemetry_settings.grafana_otlp_url}/v1/traces"
                tracer_provider = modules["TracerProvider"](resource=resource)
                tracer_provider.add_span_processor(
                    modules["BatchSpanProcessor"](
                        modules["OTLPSpanExporter"](
                            endpoint=trace_endpoint,
                            headers={"Authorization": auth_header},
                        )
                    )
                )
                modules["trace"].set_tracer_provider(tracer_provider)
                tracer_provider_registered = True
                self._tracer = modules["trace"].get_tracer(self._service_name, self._service_version)
                telemetry_connections_initialized = True
                self._logger.info("OTLP tracing exporter enabled: %s", trace_endpoint)

            if self._telemetry_settings.has_alloy_config:
                alloy_endpoint = self._build_alloy_endpoint()

                self._alloy_metrics_via_prometheus = True
                telemetry_connections_initialized = True
                self._logger.info("Alloy metrics via Prometheus /metrics scrape endpoint (instrument_fastapi_app)")

                if tracer_provider is None:
                    tracer_provider = modules["TracerProvider"](resource=resource)

                tracer_provider.add_span_processor(
                    modules["BatchSpanProcessor"](
                        modules["OTLPGrpcSpanExporter"](
                            endpoint=alloy_endpoint,
                            insecure=self._telemetry_settings.alloy_insecure,
                        )
                    )
                )

                if not tracer_provider_registered:
                    modules["trace"].set_tracer_provider(tracer_provider)
                    tracer_provider_registered = True

                self._tracer = modules["trace"].get_tracer(self._service_name, self._service_version)
                telemetry_connections_initialized = True
                self._logger.info("Alloy tracing exporter enabled: %s", alloy_endpoint)

                logger_provider = modules["LoggerProvider"](resource=resource)
                modules["_logs"].set_logger_provider(logger_provider)
                logger_provider.add_log_record_processor(
                    modules["BatchLogRecordProcessor"](
                        modules["OTLPLogExporter"](
                            endpoint=alloy_endpoint,
                            insecure=self._telemetry_settings.alloy_insecure,
                        )
                    )
                )

                handler = modules["LoggingHandler"](level=logging.INFO, logger_provider=logger_provider)
                logging.getLogger().addHandler(handler)
                telemetry_connections_initialized = True
                self._logger.info("Alloy logging exporter enabled: %s", alloy_endpoint)

            if telemetry_connections_initialized:
                self._telemetry_initialized = True
            else:
                self._logger.warning("No telemetry connection was initialized")

    def _build_basic_auth_header(self) -> str:
        credentials = base64.b64encode(
            f"{self._telemetry_settings.grafana_otlp_instance_id}:{self._telemetry_settings.grafana_cloud_api_key}".encode()
        ).decode()
        return f"Basic {credentials}"

    def _build_alloy_endpoint(self) -> str:
        return f"{self._telemetry_settings.alloy_host}:{self._telemetry_settings.alloy_port}"

    def _build_alloy_metrics_endpoint(self) -> str:
        scheme = "http" if self._telemetry_settings.alloy_insecure else "https"
        return f"{scheme}://{self._telemetry_settings.alloy_host}:{self._telemetry_settings.alloy_metrics_port}"

    def _build_resource(self):
        from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION

        return Resource.create(
            {
                SERVICE_NAME: self._service_name,
                SERVICE_VERSION: self._service_version,
                "deployment.environment": self._service_environment,
            }
        )

    def _import_telemetry_modules(self) -> dict[str, Any] | None:
        try:
            from opentelemetry import _logs, metrics, trace
            from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as OTLPGrpcSpanExporter
            from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
            from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
            from opentelemetry.sdk.metrics import MeterProvider
            from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
        except ImportError as e:
            self._logger.warning(
                "OpenTelemetry dependencies are not installed. Telemetry initialization skipped. Error: %s", e
            )
            return None

        return {
            "_logs": _logs,
            "metrics": metrics,
            "trace": trace,
            "OTLPMetricExporter": OTLPMetricExporter,
            "OTLPSpanExporter": OTLPSpanExporter,
            "OTLPGrpcSpanExporter": OTLPGrpcSpanExporter,
            "OTLPLogExporter": OTLPLogExporter,
            "LoggerProvider": LoggerProvider,
            "LoggingHandler": LoggingHandler,
            "BatchLogRecordProcessor": BatchLogRecordProcessor,
            "MeterProvider": MeterProvider,
            "PeriodicExportingMetricReader": PeriodicExportingMetricReader,
            "TracerProvider": TracerProvider,
            "BatchSpanProcessor": BatchSpanProcessor
        }
