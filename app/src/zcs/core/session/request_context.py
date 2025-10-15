import contextvars

request_context = contextvars.ContextVar("request_state", default=None)
