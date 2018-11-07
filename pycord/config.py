from contextvars import ContextVar

client = None
event = ContextVar("event")


DEFAULT_COMMAND_PARSER = "pycord.client.parser.PycordParser"
DEFAULT_ERROR_HANDLER = ""  # TODO: Make error handler
