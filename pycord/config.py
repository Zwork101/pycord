import pycord.client.commands
import pycord.client.events
import pycord.client.parser
import pycord.gateway.dispatcher
import pycord.gateway.gate

from contextvars import ContextVar

event = ContextVar("event")


COMMAND_PARSER: pycord.client.parser.PycordParser = None
ERROR_HANDLER = ""  # TODO: Make error handler
DISPATCHER: pycord.gateway.dispatcher.Dispatcher = None
GATEWAY: pycord.gateway.gate.Gateway = None
COMMAND: pycord.client.commands.Command = None
EVENT: pycord.client.events.Event = None
