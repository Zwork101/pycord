from __future__ import annotations
from typing import Optional

import pycord.config
from .base import Model


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
    """

    id: pycord.config.SNOWFLAKE
    username: str
    discriminator: str
    avatar: Optional[str]
    member: Optional[pycord.config.MEMBER]

    @property
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

    @property
    def mention(self):
        return "<@{user_id}>".format(user_id=self.id)

    @property
    def name(self):
        return "{username}#{discrim}".format(username=self.username, discrim=self.discriminator)
