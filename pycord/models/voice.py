from typing import Optional

import pycord.config
from .base import Model


class VoiceState(Model):
    """
    A voice state model to represent the people connected to voice chats

    This will be linked under VOICE_STATE. When you see people in voice channels, this is the object discord clients
    use. This isn't exclusively for guilds, I think calls use it aswell.

    :ivar guild_id: The ID of the guild the voice channel is in, if applicable
    :vartype guild_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar channel_id: The ID of the voice channel, None I think if it's a call
    :vartype channel_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar user_id: The ID of the user this voice state belongs to
    :vartype user_id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar member: The member this voice state belongs to, if applicable
    :vartype member: Optional[:py:class:`~pycord.models.guild.Guild`]
    :ivar session_id: The session ID of the user
    :vartype session_id: str
    :ivar deaf: If True, the user was deafened
    :vartype deaf: bool
    :ivar mute: If True, the user was muted
    :vartype mute: bool
    :ivar self_deaf: If True, the user deafened themselves
    :vartype self_deaf: bool
    :ivar self_mute: If True, the user muted themselves
    :vartype self_mute: bool
    :ivar suppress: If True, a priority speaking is speaking and the user's volume is decreased
    :vartype suppress: bool
    """
    guild_id: Optional[pycord.config.SNOWFLAKE]
    channel_id: Optional[pycord.config.SNOWFLAKE]
    user_id: pycord.config.SNOWFLAKE
    member: Optional[pycord.config.MEMBER]
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    suppress: bool


class VoiceRegion(Model):
    """
    A voice region model to represent the places where discord has voice servers

    This will be linked under VOICE_REGION. This is simply a way to hold information about where the server that runs
    voice channels are located.

    :ivar id: A unique ID for the server, NOT a snowflake
    :vartype id: str
    :ivar name: The name of the regeion / voice server
    :vartype name: str
    :ivar vip: If True, this is only available to partnered discord guilds
    :vartype vip: bool
    :ivar optimal: If True, this guild is closest to the user
    :vartype optimal: bool
    :ivar deprecated: If True, this server should not be connected too
    :vartype deprecated: bool
    :ivar custom: If True, this is a special voice server, used for events, whatever that would be
    :vartype custom: bool
    """
    id: str
    name: str
    vip: bool
    optimal: bool
    deprecated: bool
    custom: bool
