from typing import Optional

import pycord.config
from .base import Model


class Webhook(Model):
    """
    The pycord representation of discord webhooks

    This will be linked in the config as WEBHOOK

    :ivar id: The webhook ID
    :vartype id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar guild_id: The guild ID which this webhook is for. This may be None.
    :vartype guild_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar channel_id: The channel ID which the webhook posts in. This may be None.
    :vartype channel_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar user: The user that created the webhook. This is None when fetching for webhooks by token.
    :vartype user: Optional[:py:class:`~pycord.models.user.User`]
    :ivar name: The name of the webhook. This will be None if it doesn't have one.
    :vartype name: Optional[str]
    :ivar avatar: The avatar hash. This is None if they don't have one.
    :vartype avatar: Optional[str]
    :ivar token: The token that the webhook uses
    :vartype token: str
    """
    id: pycord.config.SNOWFLAKE
    guild_id: Optional[pycord.config.SNOWFLAKE]
    channel_id: Optional[pycord.config.SNOWFLAKE]
    user: Optional[pycord.config.USER]
    name: Optional[str]
    avatar: Optional[str]
    token: str
