import pycord
from contextvars import ContextVar

event = ContextVar("event")


COMMAND_PARSER: "pycord.client.parser.PycordParser" = None
ERROR_HANDLER: "" = ""  # TODO: Make error handler
DISPATCHER: "pycord.gateway.dispatcher.AsyncDispatcher" = None
GATEWAY: "pycord.gateway.gate.TrioGateway" = None
COMMAND: "pycord.client.commands.Command" = None
EVENT: "pycord.client.events.Event" = None

# Models
INVITE: "pycord.models.invite.Invite" = None
INVITEMETA: "pycord.models.invite.InviteMetadata" = None
SNOWFLAKE: "pycord.models.snowflake.Snowflake" = None
USER: "pycord.models.user.User" = None
OVERWRITE: "pycord.models.channel.Overwrites" = None
