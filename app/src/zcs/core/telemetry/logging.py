import logging
import queue

from zcs.core.logger import ZcsLogging
from zcs.core.session import request_context, RequestState
from zcs.core.settings.telemetry_settings import telemetry_settings


def _get_span_context():
    try:
        from opentelemetry import trace
    except ImportError:
        return None

    span_context = trace.get_current_span().get_span_context()
    if span_context and span_context.is_valid:
        return span_context

    return None


class LokiContextFilter(logging.Filter):
    """Adds per-request context as dynamic Loki tags."""

    def filter(self, record: logging.LogRecord) -> bool:
        tags = {}
        request_state: RequestState = request_context.get()
        if request_state and request_state.getOpCode():
            tags.update({
                "request_op_code": request_state.getOpCode(),
                "request_request_id": request_state.getRequestId(),
                "request_follia_module": str(request_state.getFolliaModule()),
                "auth_client_id": request_state.getAuthInfo().client_id if request_state.getAuthInfo() else None,
                "auth_tenant_id": request_state.getAuthInfo().tenant_id if request_state.getAuthInfo() else None,
                "auth_company_id": request_state.getAuthInfo().company_id if request_state.getAuthInfo() else None,
                "auth_user_id": request_state.getAuthInfo().user_id if request_state.getAuthInfo() else None,
                "auth_user_mail": request_state.getAuthInfo().user_email if request_state.getAuthInfo() else None
            })

        span_context = _get_span_context()
        if span_context:
            tags.update({
                "trace_id": format(span_context.trace_id, "032x"),
                "span_id": format(span_context.span_id, "016x"),
            })

        if tags:
            record.tags = tags

        return True


def setup_logging(logging_context: ZcsLogging, app_name: str, app_version: str, app_environment: str):

    # Grafana Cloud - Loki handler (background queue to avoid blocking)
    if telemetry_settings.has_loki_config:
        import logging_loki
        _loki_push_url = telemetry_settings.grafana_loki_url.rstrip("/")
        if not _loki_push_url.endswith("/loki/api/v1/push"):
            _loki_push_url += "/loki/api/v1/push"
        loki_handler = logging_loki.LokiQueueHandler(
            queue.Queue(-1),
            url=_loki_push_url,
            tags={
                "service": app_name,
                "env": app_environment,
                "version": app_version
            },
            auth=(telemetry_settings.grafana_loki_instance_id, telemetry_settings.grafana_cloud_api_key),
            version="1",
        )
        loki_handler.addFilter(LokiContextFilter())
        logging_context.get_logger().addHandler(loki_handler)
        logging_context.get_logger().info("Loki logging handler enabled")
    else:
        logging_context.get_logger().warning("Loki logging handler not configured")
