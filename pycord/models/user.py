from typing import Optional

from pycord.models.base import Model


class User(Model):
    """
    The pycord model for discord users.

    While the discord API says the discriminator is a string, we think it'd be more useful as an integer, especially
    as it's used to calculate the avatar_url. This will be linked in the config as USER_MODEL.

    :ivar id: The user id
    :type id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar username: The username (not including discriminator)
    :type username: str
    :ivar discriminator: The user's discriminator
    :type discriminator: int
    :ivar avatar: The hash of the user's avatar. Will be None if they don't have one.
    :type avatar: Optional[str]
    :ivar avatar_url: The url when getting their avatar. Adjusts if they don't have one or is a gif.
    :type avatar_url: str
    :ivar mention: A shortcut to mentioning a user <@123456789>
    :type mention: str
    :ivar name: The conjoined username and discriminator (for example, Test#1234)
    :type name: str
    """

    id: str  # TODO: Add snowflake object
    username: str
    discriminator: int
    avatar: Optional[str]

    @property
    def avatar_url(self):
        if self.avatar:
            if self.avatar.startswith("_a"):
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
