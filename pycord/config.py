from contextvars import ContextVar

import pycord

event = ContextVar("event")


COMMAND_PARSER: "pycord.client.parser.PycordParser" = None
DISPATCHER: "pycord.gateway.dispatcher.AsyncDispatcher" = None
GATEWAY: "pycord.gateway.gate.TrioGateway" = None
COMMAND: "pycord.client.commands.Command" = None
EVENT: "pycord.client.events.Event" = None

# Models
CHANNEL: "pycord.models.channel.Channel" = None
EMOJI: "pycord.models.emoji.Emoji" = None
GUILD: "pycord.models.guild.Guild" = None
MEMBER: "pycord.models.guild.Member" = None
ROLE: "pycord.models.guild.Role" = None
INVITE: "pycord.models.invite.Invite" = None
INVITEMETA: "pycord.models.invite.InviteMetadata" = None
ATTACHMENT: "pycord.models.message.Attachment" = None
EMBED_FOOTER: "pycord.models.message.EmbedFooter" = None
EMBED_THUMBNAIL: "pycord.models.message.EmbedThumbnail" = None
EMBED_VIDEO: "pycord.models.message.EmbedVideo" = None
EMBED_IMAGE: "pycord.models.message.EmbedImage" = None
EMBED_PROVIDER: "pycord.models.message.EmbedProvider" = None
EMBED_AUTHOR: "pycord.models.message.EmbedAuthor" = None
EMBED_FIELD: "pycord.models.message.EmbedField" = None
EMBED: "pycord.models.message.Embed" = None
MESSAGE_ACTIVITY: "pycord.models.message.MessageActivity" = None
MESSAGE_APPLICATION: "pycord.models.message.MessageApplication" = None
MESSAGE: "pycord.models.message.Message" = None
REACTION: "pycord.models.message.Reaction" = None
SNOWFLAKE: "pycord.models.snowflake.Snowflake" = None
USER: "pycord.models.user.User" = None
OVERWRITE: "pycord.models.channel.Overwrites" = None
