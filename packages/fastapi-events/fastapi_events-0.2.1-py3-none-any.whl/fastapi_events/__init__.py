from contextvars import ContextVar

__version__ = "0.2.1"

event_store = ContextVar("fastapi_context")
