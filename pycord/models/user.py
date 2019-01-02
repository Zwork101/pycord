from __future__ import annotations
from enum import Enum
from typing import Optional, Union

import pycord.config
from .base import comboproperty, Model

from combomethod import combomethod


class UserFlags(Enum):
    """
    An enum with all documented flags

    Each flag represents a group the user is associated with on discord. You can check if a user has these properties
    via the has_flag method.

    :cvar NONE: The user has no flags
    :vartype None: enum.Enum
    :cvar HYPE_SQUAD_EVENTS: The user is in HypeSquad
    :vartype HYPE_SQUAD_EVENTS: enum.Enum
    :cvar HOUSE_BRAVERY: The user is in the bravery house
    :vartype HOUSE_BRAVERY: enum.Enum
    :cvar HOUSE_BRILLIANCE: The user is in the brilliance house
    :vartype HOUSE_BRILLIANCE: enum.Enum
    :cvar HOUSE_BALANCE: The user is in the balance house
    :vartype HOUSE_BALANCE: enum.Enum
    """
    NONE = 0
    HYPE_SQUAD_EVENTS = 1 << 2
    HOUSE_BRAVERY = 1 << 6
    HOUSE_BRILLIANCE = 1 << 7
    HOUSE_BALANCE = 1 << 8


class PremiumTypes(Enum):
    """
    An enum with premium account information

    While all the enums listed have to do with nitro, discord may add more payment options that will be listed here.

    :cvar NITRO_CLASSIC: Nitro that bonuses like global emotes, but no emotes.
    :vartype NITRO_CLASSIC: enum.Enum
    :cvar NITRO: Nitro classic but with games
    :vartype NITRO: enum.Enum
    """
    NITRO_CLASSIC = 1
    NITRO = 2


class User(Model):
    """
    The pycord model for discord users.

    This will be linked in the config as USER.

    :ivar id: The user id
    :vartype id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar username: The username (not including discriminator)
    :vartype username: str
    :ivar discriminator: The user's discriminator
    :vartype discriminator: str
    :ivar avatar: The hash of the user's avatar. Will be None if they don't have one.
    :vartype avatar: Optional[str]
    :ivar avatar_url: The url when getting their avatar. Adjusts if they don't have one or is a gif.
    :vartype avatar_url: str
    :ivar mention: A shortcut to mentioning a user <@123456789>
    :vartype mention: str
    :ivar name: The conjoined username and discriminator (for example, Test#1234)
    :vartype name: str
    :ivar member: A partial member object, only available for :py:attr:`~pycord.models.message.Message.mentions`
    :vartype member: Optional[:py:class:`~pycord.models.guild.Member`]
    :ivar flags: Flags describe what groups this user is associated with on discord.
    :vartype flags: int
    :ivar premiuum_type: The ID of a this user's paid subscription, None if not applicable.
    :vartype premium_type: Optional[int]
    """

    id: pycord.config.SNOWFLAKE
    username: str
    discriminator: str
    avatar: Optional[str]
    member: Optional[pycord.config.MEMBER]
    flags: int
    premium_type: Optional[int]

    @comboproperty
    def avatar_url(self):
        if self.avatar:
            if self.avatar.startswith("a_"):
                return "https://cdn.discordapp.com/avatars/{user_id}/{user_avatar}.gif".format(
                    user_id=self.id,
                    user_avatar=self.avatar
                )
            else:
                return "https://cdn.discordapp.com/avatars/{user_id}/{user_avatar}.png".format(
                    user_id=self.id,
                    user_avatar=self.avatar
                )
        return "https://cdn.discordapp.com/embed/avatars/{discrim}.png".format(discrim=self.discriminator % 5)

    @comboproperty
    def mention(self):
        return "<@{user_id}>".format(user_id=self.id)

    @comboproperty
    def name(self):
        return "{username}#{discrim}".format(username=self.username, discrim=self.discriminator)

    @combomethod
    def has(self, flag_or_premium: Union[UserFlags, PremiumTypes]):
        """
        This method is used to check if a user has a certain attribute

        This method is used to check if a user belongs to a group such as hypesquad, or is subscribed to some version
        of nitro. You will have to use the enums provided in the ``pycord.models.user`` file.

        :param flag_or_premium: An enum with for user flags, or a enum for nitro
        :type flag_or_premium: Union[:py:class:`~pycord.models.user.UserFlags`, :py:class:`~pycord.models.user.PremiumTypes`]
        :return: True if the user does have the service else False
        :rtype: bool
        """
        if flag_or_premium in UserFlags:
            if flag_or_premium.value & self.flags:
                return True
        elif flag_or_premium in PremiumTypes:
            if flag_or_premium.value == self.premium_type:
                return True
        else:
            raise ValueError("Value provided was not in UserFlags enum nor PremiumTypes enum.")
        return False
