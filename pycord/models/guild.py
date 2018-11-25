from __future__ import annotations
from typing import List, Optional

import pycord.config
from pycord.helpers import parse_timestamp
from .base import Model


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

    @property
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

    @property
    def join_date(self):
        return parse_timestamp(self.joined_at)

    @property
    def mention(self):
        if self.nick:
            return "<@!{user_id}>".format(user_id=self.user.id)
        else:
            return self.user.mention


class Guild(Model):
    pass
