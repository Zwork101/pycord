from contextvars import ContextVar
from typing import Type

import pycord

event = ContextVar("event")


COMMAND_PARSER: "Type[pycord.client.parser.PycordParser]" = None
DISPATCHER: "Type[pycord.gateway.dispatcher.AsyncDispatcher]" = None
GATEWAY: "Type[pycord.gateway.gate.TrioGateway]" = None
COMMAND: "Type[pycord.client.commands.PycordCommand]" = None

# Models
CHANNEL: "Type[pycord.models.channel.Channel]" = None
EMOJI: "Type[pycord.models.emoji.Emoji]" = None
ACTIVITY_TIMESTAMP: "Type[pycord.models.gateway.ActivityTimestamps]" = None
ACTIVITY_PARTY: "Type[pycord.models.gateway.ActivityParty]" = None
ACTIVITY_ASSETS: "Type[pycord.models.gateway.ActivityAssets]" = None
ACTIVITY_SECRETS: "Type[pycord.models.gateway.ActivitySecrets]" = None
ACTIVITY: "Type[pycord.models.gateway.Activity]" = None
PRESENCE_UPDATE: "Type[pycord.models.gateway.PresenceUpdate]" = None
GUILD: "Type[pycord.models.guild.Guild]" = None
MEMBER: "Type[pycord.models.guild.Member]" = None
ROLE: "Type[pycord.models.guild.Role]" = None
INVITE: "Type[pycord.models.invite.Invite]" = None
INVITEMETA: "Type[pycord.models.invite.InviteMetadata]" = None
ATTACHMENT: "Type[pycord.models.message.Attachment]" = None
EMBED_FOOTER: "Type[pycord.models.message.EmbedFooter]" = None
EMBED_THUMBNAIL: "Type[pycord.models.message.EmbedThumbnail]" = None
EMBED_VIDEO: "Type[pycord.models.message.EmbedVideo]" = None
EMBED_IMAGE: "Type[pycord.models.message.EmbedImage]" = None
EMBED_PROVIDER: "Type[pycord.models.message.EmbedProvider]" = None
EMBED_AUTHOR: "Type[pycord.models.message.EmbedAuthor]" = None
EMBED_FIELD: "Type[pycord.models.message.EmbedField]" = None
EMBED: "Type[pycord.models.message.Embed]" = None
MESSAGE_ACTIVITY: "Type[pycord.models.message.MessageActivity]" = None
MESSAGE_APPLICATION: "Type[pycord.models.message.MessageApplication]" = None
MESSAGE: "Type[pycord.models.message.Message]" = None
REACTION: "Type[pycord.models.message.Reaction]" = None
SNOWFLAKE: "Type[pycord.models.snowflake.Snowflake]" = None
USER: "Type[pycord.models.user.User]" = None
VOICE_STATE: "Type[pycord.models.voice.VoiceState]" = None
VOICE_REGION: "Type[pycord.models.voice.VoiceRegion]" = None
OVERWRITE: "Type[pycord.models.channel.Overwrites]" = None
