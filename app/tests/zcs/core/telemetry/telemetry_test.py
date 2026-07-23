import logging

from zcs.core.settings.telemetry_settings import TelemetrySettings
from zcs.core.telemetry.zcs_telemetry import ZcsTelemetry


def test_telemetry_settings_otlp_and_loki_flags() -> None:
    settings = TelemetrySettings(
        grafana_otlp_url="https://example.com",
        grafana_loki_url="https://loki.example.com",
        grafana_cloud_api_key="token",
    )

    assert settings.has_otlp_config
    assert settings.has_loki_config


def _prometheus_alloy_telemetry() -> ZcsTelemetry:
    telemetry = object.__new__(ZcsTelemetry)
    telemetry._telemetry_initialized = True
    telemetry._alloy_metrics_via_prometheus = True
    telemetry._meters = {}
    telemetry._custom_metrics = {}
    telemetry._prometheus_counters = {}
    telemetry._logger = logging.getLogger(__name__)
    return telemetry


def test_counter_create_with_label_names_allows_labeled_counter_add() -> None:
    telemetry = _prometheus_alloy_telemetry()

    telemetry.counter_create(
        name="labeled_counter_test",
        unit="1",
        description="test counter with labels",
        label_names=["sender"],
    )
    telemetry.counter_add("labeled_counter_test", {"sender": "123"})

    counter = telemetry._prometheus_counters["labeled_counter_test"]
    assert counter.labels(sender="123")._value.get() == 1


def test_counter_create_without_label_names_allows_unlabeled_counter_add() -> None:
    telemetry = _prometheus_alloy_telemetry()

    telemetry.counter_create(
        name="unlabeled_counter_test",
        unit="1",
        description="test counter without labels",
    )
    telemetry.counter_add("unlabeled_counter_test")

    counter = telemetry._prometheus_counters["unlabeled_counter_test"]
    assert counter._value.get() == 1
