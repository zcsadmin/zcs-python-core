from collections.abc import Mapping
from typing import Any

from zcs.core.session import RequestState, request_context


def _safe_set_attribute(span, key: str, value: Any) -> None:
    if value is None:
        return

    if isinstance(value, (str, bool, int, float)):
        span.set_attribute(key, value)
        return

    span.set_attribute(key, str(value))


def set_trace_attributes(
    request_state: RequestState | None = None,
    *,
    app_name: str | None = None,
    app_environment: str | None = None,
    app_version: str | None = None,
    extra_attributes: Mapping[str, Any] | None = None,
) -> None:
    """Set trace attributes from app metadata and request context."""
    try:
        from opentelemetry import trace
    except ImportError:
        return

    span = trace.get_current_span()
    if not span:
        return

    span_context = span.get_span_context()
    if not span_context or not span_context.is_valid:
        return

    current_state = request_state or request_context.get()

    _safe_set_attribute(span, "app_name", app_name)
    _safe_set_attribute(span, "app_environment", app_environment)
    _safe_set_attribute(span, "app_version", app_version)

    if not current_state:
        if extra_attributes:
            for key, value in extra_attributes.items():
                _safe_set_attribute(span, key, value)
        return

    _safe_set_attribute(span, "request_op_code", current_state.getOpCode())
    _safe_set_attribute(span, "request_request_id", current_state.getRequestId())
    _safe_set_attribute(span, "request_follia_module", current_state.getFolliaModule())

    auth_info = current_state.getAuthInfo()
    if auth_info:
        _safe_set_attribute(span, "auth_client_id", auth_info.client_id)
        _safe_set_attribute(span, "auth_tenant_id", auth_info.tenant_id)
        _safe_set_attribute(span, "auth_company_id", auth_info.company_id)
        _safe_set_attribute(span, "auth_user_id", auth_info.user_id)
        _safe_set_attribute(span, "auth_user_mail", auth_info.user_email)

    if extra_attributes:
        for key, value in extra_attributes.items():
            _safe_set_attribute(span, key, value)
