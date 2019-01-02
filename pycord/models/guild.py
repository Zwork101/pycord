from __future__ import annotations
from typing import List, Optional

import pycord.config
from pycord.helpers import parse_timestamp
from .base import comboproperty, Model


class Role(Model):
    """
    This role model is used to represent discord roles

    This is linked under ROLE. A role is used to group certain people, or add permissions to them.

    :ivar id: The ID of the role
    :vartype id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar name: The name of the role
    :vartype name: str
    :ivar color: A number that's representing a color, like 0xFFFFFF is white
    :vartype color: int
    :ivar hoist: If True, people who have the role will be displayed separately from others
    :varype hoist: bool
    :ivar position: The position this role exists in, from other roles
    :vartype position: int
    :ivar permissions: A bitset that add to a user's permissions
    :vartype permissions: int
    :ivar managed: This will only be False if the role is added by discord for a bot's initial permissions
    :vartype managed: bool
    :ivar mentioned: If True, people can mention this role
    :vartype mentioned: bool
    :ivar mention: A mention of the role, will provide even if it isn't mentionable
    :vartype mention: str
    """
    id: pycord.config.SNOWFLAKE
    name: str
    color: int
    hoist: bool
    position: int
    permissions: int
    managed: bool
    mentioned: bool

    @comboproperty
    def mention(self):
        return "<@&{role_id}>".format(role_id=self.id)


class Member(Model):
    """
    This member model represents discord members

    This is linked under MEMBER. A member is simply a normal user with guild specific information. There will be no way
    to find the original guild from a member object unless it's received from a gateway event such as when a user joins
    a guild.

    :ivar user: The user that this member represents
    :vartype user: :py:class:`~pycord.models.user.User`
    :ivar nick: The nickname this member has, None if they don't have one
    :vartype nick: Optional[str]
    :ivar roles: A list of snowflakes linking to roles the member has
    :vartype roles: List[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar joined_at: An ISO8601 timestamp for when the user joined
    :vartype joined_at: str
    :ivar join_date: A parsed version of the joined_at property
    :vartype join_date: datetime.datetime
    :ivar deaf: If True, the user can't hear the VC on the guild
    :vartype deaf: bool
    :ivar mute: If True, the user can't speak on the VC in the guild
    :vartype mute: bool
    :ivar mention: Much like :py:attr:`~pycord.models.user.User.mention`, however this takes into account a user's nick
    :vartype mention: str
    :ivar guild_id: The guild ID the member belongs to. Only available on events where a member does something like join
    :vartype guild_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    """
    user: pycord.config.USER
    nick: Optional[str]
    roles: List[pycord.config.SNOWFLAKE]
    joined_at: str
    deaf: bool
    mute: bool
    guild_id: Optional[pycord.config.SNOWFLAKE]

    @comboproperty
    def join_date(self):
        return parse_timestamp(self.joined_at)

    @comboproperty
    def mention(self):
        if self.nick:
            return "<@!{user_id}>".format(user_id=self.user.id)
        else:
            return self.user.mention


class Guild(Model):
    """
    The guild model to represent discord guilds (servers)

    This will be linked under GUILD. Keep in mind that, joined_at, large, unavailable, member_count, voice_states,
    members, channels, and presences, will only be available when on GUILD_CREATE events. I didn't bother making enums
    for the types like default_message_notifications, because they're not really that useful for bots.

    :ivar id: The ID of the guild
    :vartype id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar name: The name of the guild
    :vartype name: str
    :ivar icon: The image hash of the guild icon
    :vartype icon: Optional[str]
    :ivar icon_url: A URL leading to the image with the guild icon
    :vartype icon_url: Optional[str]
    :ivar splash: The image hash of the background for invites
    :vartype splash: Optional[str]
    :ivar splash_url: A url to the splash image
    :vartype splash_url: Optional[str]
    :ivar owner: If True, you own this server
    :vartype owner: Optional[bool]
    :ivar owner_id: The ID of the person who owns the server
    :vartype owner_id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar permissions: A compiled bitset of this user's current permissions without channel overwrites
    :vartype permissions: Optional[int]
    :ivar region: Where the server that manages voice chats are held
    :vartype region: str
    :ivar afk_channel_id: The ID of the voice channel where AFK people are put
    :vartype afk_channel_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar afk_timeout: How much inactivity until they're moved to an afk channel in seconds
    :vartype afk_timeout: int
    :ivar embed_enabled: If True, the guild can be embedable into websites
    :vartype embed_enabled: Optional[bool]
    :ivar embed_channel_id: The ID of the channel used when embeding if applicable
    :vartype embed_channel_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar verification_level: A number representing how strict the server security is
    :vartype verification_level: int
    :ivar default_message_notifications: A number to represent if messages notify users
    :vartype default_message_notifications: int
    :ivar explicit_content_filter: If True, discord will remove naughty messages
    :vartype explicit_content_filter: int
    :ivar roles: A list of roles on the guild
    :vartype roles: List[:py:class:`~pycord.models.guild.Role`]
    :ivar emojis: A list of emojis the guild has made
    :vartype emojis: List[:py:class:`~pycord.models.emoji.Emoji`]
    :ivar features: Enabled guild features, whatever that means
    :vartype features: List[str]
    :ivar mfa_level: If 1, you need to have 2fac to use some admin powers
    :vartype mfa_level: int
    :ivar application_id: The ID of the bot that made the guild, if applicable
    :vartype application_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar widget_enabled: If True, this guild can a widget
    :vartype widget_enabled: Optional[bool]
    :ivar widget_channel_id: The channel ID for the widget, if applicable
    :vartype widget_channel_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar system_channel_id: The channel ID where system messages will be sent (like join messages)
    :vartype system_channel_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar joined_at: An ISO8601 timestamp for when the user joined
    :vartype joined_at: Optional[str]
    :ivar joined_at_date: A parsed version of the ISO timestamp, not reliable
    :vartype joined_at_date: Optional[datetime.datetime]
    :ivar large: If True, this guild is considered large
    :vartype large: Optional[bool]
    :ivar unavailable: If True, this guild is deleted or something
    :vartype unavailable: Optional[bool]
    :ivar member_count: An estimate towards the amount of people in the guild
    :vartype member_count: Optional[int]
    :ivar voice_states: A list of information about the current people using voice chats
    :vartype voice_states: Optional[List[:py:class:`~pycord.models.voice.VoiceState`]]
    :ivar members: A list of the current members, may not be full depending on server size
    :vartype mmebers: Optional[List[:py:class:`~pycord.models.guild.Memebr`]]
    :ivar channels: A list of channels (text and voice) on the guild
    :vartype channels: Optional[List[:py:class:`~pycord.models.channel.Channel`]]
    :ivar presences: A list of presences for the people in the guild, may not be complete
    :vartype presences: Optional[List[:py:class:`~pycord.models.gateway.PresenceUpdate`]]
    """
    id: pycord.config.SNOWFLAKE
    name: str
    icon: Optional[str]
    splash: Optional[str]
    owner: Optional[bool]
    owner_id: pycord.config.SNOWFLAKE
    permissions: Optional[int]
    region: str
    afk_channel_id: Optional[pycord.config.SNOWFLAKE]
    afk_timeout: int
    embed_enabled: Optional[bool]
    embed_channel_id: Optional[pycord.config.SNOWFLAKE]
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    roles: List[pycord.config.ROLE]
    emojis: List[pycord.config.EMOJI]
    features: List[str]
    mfa_level: int
    application_id: Optional[pycord.config.SNOWFLAKE]
    widget_enabled: Optional[bool]
    widget_channel_id: Optional[pycord.config.SNOWFLAKE]
    system_channel_id: Optional[pycord.config.SNOWFLAKE]
    joined_at: Optional[str]
    large: Optional[bool]
    unavailable: Optional[bool]
    member_count: Optional[int]
    voice_states: Optional[List[pycord.config.VOICE_STATE]]
    members: Optional[List[pycord.config.MEMBER]]
    channels: Optional[List[pycord.config.CHANNEL]]
    presences: Optional[List[pycord.config.PRESENCE_UPDATE]]

    @comboproperty
    def icon_url(self):
        if self.icon:
            return "https://cdn.discordapp.com/icons/{guild_id}/{guild_icon}.png".format(
                guild_id=self.id,
                guild_icon=self.icon
            )

    @comboproperty
    def splash_url(self):
        if self.splash:
            return "https://cdn.discordapp.com/splashes/{guild_id}/{guild_splash}.png".format(
                guild_id=self.id,
                guild_splash=self.splash
            )

    @comboproperty
    def joined_at_date(self):
        return parse_timestamp(self.joined_at) if self.joined_at else None
