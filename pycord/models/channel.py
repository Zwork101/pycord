from __future__ import annotations

from enum import Enum
from typing import List, Optional

import pycord.config
from pycord.helpers import parse_timestamp
from .base import Model


class Overwrites(Model):
    """
    The overwrite model of the discord overwrites

    This will be linked under OVERWRITE. Overwrites are used for calculating permissions. Users can create overwrites
    to change a user or role's permissions for a specific channel.

    :ivar id: The id of the overwrite object
    :vartype id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar type: The type of overwrite, will either be "role" or "member"
    :vartype type: str
    :ivar allow: A bitset containing all the perms that are allowed
    :vartype allow: int
    :ivar deny: A bitset containing all the perms that are not allowed
    :vartype deny: int
    """
    id: pycord.config.SNOWFLAKE
    type: str
    allow: int
    deny: int


class ChannelTypes(Enum):
    """
    A list of channel types.

    :cvar GUILD_TEXT: A text channel that belongs to a guild
    :vartype GUILD_TEXT: enum.Enum
    :cvar DM: A channel that belongs to a direct message
    :vartype DM: enum.Enum
    :cvar GUILD_VOICE: A voice channel that belongs toa guild
    :vartype GUILD_VOICE: enum.Enum
    :cvar GROUP_DM: A channel that belongs to a group direct message
    :vartype GROUP_DM: enum.Enum
    :cvar GUILD_CATEGORY: A channel category class
    :vartype GUILD_CATEGORY: enum.Enum
    """
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4


class Channel(Model):
    """
    The channel model of the discord channels

    This will be liked under CHANNEL. Because of the way discord works, it sends text channels and voice channels as the
    same object. It's up to you to either check the type property, or just know what to expect.

    :ivar id: The ID discord gave the channel
    :vartype id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar type: The type of discord object represented with a number
    :vartype type: int
    :ivar channel_type: The parsed channel type
    :vartype channel_type: enum.EnumMeta
    :ivar guild_id: The ID of the guild in which this channel belongs too
    :vartype guild_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar position: The position this channel is, in the order of channels
    :vartype position: Optional[int]
    :ivar permission_overwrites: A list of overwrites effecting peoples' and roles' permissions in the channel
    :vartype permission_overwrites: Optional[List[:py:class:`~pycord.models.channel.Overwrite`]]
    :ivar name: The name of the channel
    :vartype name: Optional[str]
    :ivar topic: The channel's description
    :vartype topic: Optional[str]
    :ivar nsfw: A boolean on whether the channel allows nsfw content or not
    :vartype nsfw: Optional[bool]
    :ivar last_message_id: The ID of the last message sent into the channel. This will NOT be updated live
    :vartype last_message_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar bitrate: The current bitrate. This is the amount of data that is allowed to be sent at once (for voice only)
    :vartype bitrate: Optional[int]
    :ivar user_limit: The amount of users allowed in the voice channel at once
    :vartype user_limit: Optional[int]
    :ivar rate_limit_per_user: This is slowmode, defining how long it is between messages for people talking in it
    :vartype rate_limit_per_user: Optional[int]
    :ivar recipients: A list of people in the group DM
    :vartype recipients: Optional[List[:py:class:`~pycord.models.user.User`]]
    :ivar icon: The hash of the icon image used for a group DM
    :vartype icon: Optional[str]
    :ivar owner_id: The user ID of the user whom made the DM
    :vartype owner_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar application_id: If the DM was created by a bot, this is the bot's ID
    :vartype application_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar parent_id: The category ID that the channel belongs too
    :vartype parent_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar last_pin_timestamp: The timestamp of the message that was last pinned
    :vartype last_pin_timestamp: Optional[str]
    :ivar last_pin_date: A parsed version of the last_pin_timestamp. This is possibly unreliable and inacurate, use arrow or dateutils
    :vartype last_pin_date: Optional[datetime.datetime]
    """
    id: pycord.config.SNOWFLAKE
    type: int
    guild_id: Optional[pycord.config.SNOWFLAKE]
    position: Optional[int]
    permission_overwrites: Optional[List[pycord.config.OVERWRITE]]
    name: Optional[str]
    topic: Optional[str]
    nsfw: Optional[bool]
    last_message_id: Optional[pycord.config.SNOWFLAKE]
    bitrate: Optional[int]
    user_limit: Optional[int]
    rate_limit_per_user: Optional[int]
    recipients: Optional[List[pycord.config.USER]]
    icon: Optional[str]
    owner_id: Optional[pycord.config.SNOWFLAKE]
    application_id: Optional[pycord.config.SNOWFLAKE]
    parent_id: Optional[pycord.config.SNOWFLAKE]
    last_pin_timestamp: Optional[str]

    @property
    def channel_type(self):
        for channel_type in ChannelTypes:
            if channel_type.value == self.type:
                return channel_type

    @property
    def last_pin_date(self):
        return parse_timestamp(self.last_pin_timestamp) if self.last_pin_timestamp else None
