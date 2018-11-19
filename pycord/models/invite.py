from datetime import datetime
from typing import Optional

from .base import Model
from .channel import Channel
from .guild import Guild
from .user import User
from pycord.helpers import parse_timestamp


class Invite(Model):
    """
    The invite models of the discord invites

    This will be linked under INVITE.

    :ivar code: The invite code
    :vartype code: str
    :ivar guild: The guild the invite links too
    :vartype guild: Optional[:py:class:`~pycord.models.guild.Guild`]
    :ivar channel: The channel this invite was created for
    :vartype channel: :py:class:`~pycord.models.channel.Channel`
    :ivar approximate_presence_count: The approximate amount of people currently online in the server
    :vartype approximate_presence_count: Optional[int]
    :ivar approximate_member_count: The approximate amount of people actually in the server
    :vartype approximate_member_count: Optional[int]
    """
    code: str
    guild: Optional[Guild]
    channel: Optional[Channel]
    approximate_presence_count = Optional[int]
    approximate_member_count = Optional[int]


class InviteMetadata(Model):
    """
    The invite meta data for a discord invite

    This will be linked under INVITEMETA. Keep in mind, if you need a reliable way to get the creation date of the
    in, don't use creation_date. That's a hacky method, and it's advised you use something like dateutil or arrow to
    parse the created_at property (an ISO timestamp).

    :ivar inviter: The user of created the invite
    :vartype inviter: :py:class:`~pycord.models.user.User`
    :ivar uses: The amount of time people have joined with this invite
    :vartype uses: int
    :ivar max_uses: The amount of times this invite can be used before expiring (0 if there is no expiration)
    :vartype max_uses: int
    :ivar max_age: The amount of time it will take until the invite expires in seconds
    :vartype max_age: int
    :ivar temporary: If True, people that use this invite will be forced to leave after a while
    :vartype temporary: bool
    :ivar created_at: The date this invite was created in the form of an ISO8601 timestamp
    :vartype created_at: str
    :ivar creation_date: A parsed version of created_at, however is not stable. dateutil or arrow is advised.
    :vartype creation_date: datetime.datetime
    :ivar revoked: If True, this invite has expired and can't be used
    :vartype revoked: bool
    """
    inviter: User
    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: str
    revoked: bool

    @property
    def creation_date(self):
        return parse_timestamp(self.created_at)
