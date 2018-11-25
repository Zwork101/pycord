from __future__ import annotations
from typing import List, Optional

import pycord.config
from .base import Model


class Emoji(Model):
    """
    This emoji model is used to represent emojis used on discord

    This will be linked under EMOJI. This is one of the few models where the ID can be None. It's None when the emoji
    is a normal unicode one, and not an emoji that was added by someone.

    :ivar id: The ID of the emoji if applicable
    :vartype id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar name: The name of the emoji. If it's a normal unicode emoji, name will be the actual emoji
    :vartype name: str
    :ivar roles: A list of roles that can only use the emoji
    :vartype roles: Optional[List[:py:class:`~pycord.models.guild.Role`]]
    :ivar user: The user that created the emoji if applicable
    :vartype user: Optional[:py:class:`~pycord.models.user.User`]
    :ivar require_colons: If True, this emoji is custom and needs to be like :LUL:
    :vartype require_colons: Optional[bool]
    :ivar managed: Uhhhh, I have no idea. I guess emojis discord adds that aren't unicode?
    :vartype managed: Optional[bool]
    :ivar animated: If True, this emoji is animated
    :vartype animated: Optional[bool]
    :ivar text: A formatted string that discord will change into an emoji
    :vartype text: str
    """
    id: Optional[pycord.config.SNOWFLAKE]
    name: str
    roles: Optional[List[pycord.config.SNOWFLAKE]]
    user: Optional[pycord.config.USER]
    require_colons: Optional[bool]
    managed: Optional[bool]
    animated: Optional[bool]

    @property
    def text(self):
        if not self.id:
            return self.name
        if self.animated:
            return "<a:{name}:{emoji_id}>".format(name=self.name, emoji_id=self.id)
        return "<{name}:{emoji_id}>".format(name=self.name, emoji_id=self.id)
