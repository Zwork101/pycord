from __future__ import annotations
from enum import Enum
from typing import List, Optional

import pycord.config
from pycord.helpers import parse_timestamp
from .base import Model


class MessageTypes(Enum):
    """
    An enum with all the different types of messages

    You may be surprised to see that there are different message types. That's because discord notifications like when a
    user joins, or a message is pinged, those are actually messages sent by discord. Weird choice but ok. DEFAULT is
    your normal message type.

    :cvar DEFAULT: A normal message sent by a user
    :vartype DEFAULT: enum.Enum
    :cvar RECIPIENT_ADD: A message sent when someone is added to a group DM
    :vartype RECIPIENT_ADD: enum.Enum
    :cvar RECIPIENT_REMOVE: A message sent when someone is removed from a group DM
    :vartype RECIPIENT_REMOVE: enum.Enum
    :cvar CALL: A message sent to signify when a user has been called
    :vartype CALL: enum.Enum
    :cvar CHANNEL_NAME_CHANGE: A message sent when the channel's name has been changed
    :vartype CHANNEL_NAME_CHANGE: enum.Enum
    :cvar CHANNEL_ICON_CHANGE: A message sent when a channel's icon has been chnaged
    :vartype CHANNEL_ICON_CHANGE: enum.Enum
    :cvar CHANNEL_PINNED_MESSAGE: A message sent when a user pins a message
    :vartype CHANNEL_PINNED_MESSAGE: enum.Enum
    :cvar GUILD_MEMBER_JOIN: A message sent when someone joins, can be disabled
    :vartype GUILD_MEMBER_JOIN: enum.Enum
    """
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7


class MessageActivityType(Enum):
    """
    An enum with all the different types of message activities

    Sometimes, discord might send magical messages. These might be like links to join a spotify song.

    :cvar JOIN: A special message asking people to join a game
    :vartype JOIN: enum.Enum
    :cvar SPECTATE: A special message asking people to spectate a game
    :vartype SPECTATE: enum.Enum
    :cvar LISTEN: A special message asking people to listen to songs together
    :vartype LISTEN: enum.Enum
    :cvar JOIN_REQUEST: I have no idea, it's just another activity
    :vartype JOIN_REQUEST: enum.Enum
    """
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 4


class MessageActivity(Model):
    """
    The message activity model to represent a message's activity (if applicable)

    This will be linked under MESSAGE_ACTIVITY. It's used on the discord client to send special messages. These
    messages might invite someone to a game, or have them join a party.

    :ivar type: This is a number representing the activity type.
    :vartype type: int
    :ivar activity_type: This is a parsed version of the type, returning an enum from :py:class:`~pycord.models.message.MessageActivityType`
    :vartype activity_type: enum.Enum
    :ivar party_id: The party_id will be used to allow discord to put you into the game
    :vartype party_id: Optional[str]
    """
    type: int
    party_id: Optional[str]

    @property
    def activity_type(self):
        for activity in MessageActivityType:
            if activity.value == self.type:
                return activity


class MessageApplication(Model):
    """
    The message application model to represent fancy discord message stuff

    This will be linked under MESSAGE_APPLICATION. I'm really not sure what this is, but it's documented to an extent,
    so whatever.

    :ivar id: The message application ID
    :vartype id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar cover_image: An asset ID for the cover image
    :vartype cover_image: str
    :ivar description: The description of the message application
    :vartype description: str
    :ivar icon: An asset ID for the icon
    :vartype icon: str
    :ivar name: The name of the message application
    :vartype name: str
    """
    id: pycord.config.SNOWFLAKE
    cover_image: str
    description: str
    icon: str
    name: str


class Attachment(Model):
    """
    This attachment model is used to represent discord message attachments

    This will be linked under ATTACHMENT. This is used for messages that have files such as images.

    :ivar id: A snowflake that was designated to the attachment
    :vartype id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar filename: The name of the uploaded file
    :vartype filename: str
    :ivar size: The size of the file in bytes
    :vartype size: int
    :ivar url: A url that leads to the original file
    :vartype url: str
    :ivar proxy_url: A url that uses discord as a proxy to the file
    :vartype proxy_url: str
    :ivar height: If the file is an image, this contains the height of the image
    :vartype height: Optional[int]
    :ivar width: If the file is an image, this contains the width of the image
    :vartype width: Optional[int]
    """
    id: pycord.config.SNOWFLAKE
    filename: str
    size: int
    url: str
    proxy_url: str
    height: Optional[int]
    width: Optional[int]


class EmbedThumbnail(Model):
    """
    This thumbnail model is used to represent thumbnail images on embeds

    This will be linked under EMBED_THUMBNAIL. Thumbnails are the tiny icons you see at the top of an embed.

    :ivar url: A url to the file which will be the thumbnail image
    :vartype url: Optional[url]
    :ivar proxy_url: A url that uses the discord proxy to hold the file
    :vartype proxy_url: Optional[str]
    :ivar height: The height of the file image
    :vartype height: Optional[int]
    :ivar width: The width of the file image
    :vartype width: Optional[int]
    """
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedVideo(Model):
    """
    This video model is used to represent videos on embeds

    This will be linked under EMBED_VIDEO. Video embeds are used for embedding things such as youtube.com and twitch.tv.

    :ivar url: A url to the place where the video is located, such as youtube, or twitch
    :vartype url: Optional[url]
    :ivar height: The height of the video
    :vartype height: Optional[int]
    :ivar width: The width of the video
    :vartype width: Optional[int]
    """
    url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedImage(Model):
    """
    This image model is used to represent images on embeds

    This will be linked under EMBED_IMAGE. Image embeds are used for embedding images from stuff like giphy.

    :ivar url: A url to the place where the image is located, such as giphy
    :vartype url: Optional[str]
    :ivar proxy_url: A url that uses the discord proxy to hold the file
    :vartype proxy_url: Optional[str]
    :ivar height: The height of the image
    :vartype height: Optional[int]
    :ivar width: The width of the image
    :vartype width: Optional[int]
    """
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedProvider(Model):
    """
    This provider model is used to represent provider properties on discord embeds

    This will be linked under EMBED_PROVIDER. Providers are used to show where an embed's source comes from.

    :ivar name: The name of the embed provider
    :vartype name: Optional[str]
    :ivar url: The url to the embed provider
    :vartype url: Optional[str]
    """
    name: Optional[str]
    url: Optional[str]


class EmbedAuthor(Model):
    """
    This author model is used to represent the author of discord embeds

    This will be linked under EMBED_AUTHOR. Authors are small icons with a name, that can lead to a url.

    :ivar name: The name of the author
    :vartype name: Optional[str]
    :ivar url: A url that can be clicked on the embed from the name
    :vartype url: Optional[str]
    :ivar icon_url: A url to the image for the author's icon
    :vartype icon_url: Optional[str]
    :ivar icon_proxy_url: A url for the image that goes through discord first
    :vartype icon_proxy_url: Optional[str]
    """
    name: Optional[str]
    url: Optional[str]
    icon_url: Optional[str]
    icon_proxy_url: Optional[str]


class EmbedFooter(Model):
    """
    This footer model is used to represent a discord embed's footer

    This will be linked under EMBED_FOOTER. Footers are the small text you see at the bottom of an embed.

    :ivar text: The footer text. Unlike many other embed properties, this will always be a string.
    :vartype text: str
    :ivar icon_url: A url that links to a small image for the bottom left of an embed
    :vartype icon_url: Optional[str]
    :ivar icon_proxy_url: A url that is linked to discord which has the icon_url
    :vartype icon_proxy_url: Optional[str]
    """
    text: str
    icon_url: Optional[str]
    icon_proxy_url: Optional[str]


class EmbedField(Model):
    """
    This field model is used to represent fields on discord embeds

    This will be linked under EMBED_FIELD. Fields are little boxes on embeds that has a name + description.

    :ivar name: The name of the field, this is at the top and semi-bolded
    :vartype name: str
    :ivar value: The text below the name, not bolded
    :vartype value: str
    :ivar inline: If True, it will be organized better with the other fields
    :vartype inline: Optional[bool]
    """
    name: str
    value: str
    inline: Optional[bool]


class Embed(Model):
    """
    This embed model is used to represent embeds on discord messages

    This will be linked under EMBED. If you want more information about properties such as the footer or author, see
    it's class. Embeds are those fancy boxes you see in chat that can have links, colors, etc.

    :ivar title: The title of the embed, that can be found at the top
    :vartype title: Optional[str]
    :ivar type: The type of embed
    :vartype type: Optional[str]
    :ivar description: The description of the embed, this will be the body of it, formatting is allowed
    :vartype description: Optional[str]
    :ivar url: The url that will be opened when someone clicks the title
    :vartype url: Optional[str]
    :ivar timestamp: An ISO8601 timestamp, which will be displayed near the footer
    :vartype timestamp: Optional[str]
    :ivar timestamp_date: A parsed version of timestamp, will be None if timestamp isn't provided
    :vartype timestamp_date: Optional[datetime.datetime]
    :ivar color: A number representing a color. For example, 0xFFA500 is orange
    :vartype color: Optional[int]
    :ivar footer: Text at the bottom of an embed that can have an icon
    :vartype footer: Optional[:py:class:`~pycord.models.message.EmbedFooter`]
    :ivar image: An image attached to the embed
    :vartype image: Optional[:py:class:`~pycord.models.message.EmbedImage`]
    :ivar thumbnail: A thumbnail that is located at the top left
    :vartype thumbnail: Optional[:py:class:`~pycord.models.message.EmbedThumbnail`]
    :ivar video: A video that is attached to the embed
    :vartype video: Optional[:py:class:`~pycord.models.message.EmbedVideo`]
    :ivar provider: The person / site that provided the embed
    :vartype provider: Optional[:py:class:`~pycord.models.message.EmbedProvider`]
    :ivar author: The author of the embed, can be anyone
    :vartype author: Optional[:py:class:`~pycord.models.message.EmbedAuthor`]
    :ivar fields: A list of fields that will be on the body of the embed
    :vartype fields: Optional[List[:py:class:`~pycord.models.message.EmbedField`]]
    """
    title: Optional[str]
    type: Optional[str]
    description: Optional[str]
    url: Optional[str]
    timestamp: Optional[str]
    color: Optional[int]
    footer: Optional[pycord.config.EMBED_FOOTER]
    image: Optional[pycord.config.EMBED_IMAGE]
    thumbnail: Optional[pycord.config.EMBED_THUMBNAIL]
    video: Optional[pycord.config.EMBED_VIDEO]
    provider: Optional[pycord.config.EMBED_PROVIDER]
    author: Optional[pycord.config.EMBED_AUTHOR]
    fields: Optional[List[pycord.config.EMBED_FIELD]]

    @property
    def timestamp_date(self):
        return parse_timestamp(self.timestamp) if self.timestamp else None


class Reaction(Model):
    """
    This reaction model is use to represent reactions on discord messages

    This will be linked under REACTION. This is simply an object that holds an emoji along side the amount of reactions.

    :ivar count: The amount of reactions for a certain emoji
    :vartype count: int
    :ivar me: If True, you've already reacted
    :vartype me: bool
    :ivar emoji: The emoji that's being used to react
    :vartype emoji: :py:class:`~pycord.models.emoji.Emoji`
    """
    count: int
    me: bool
    emoji: pycord.config.EMOJI


class Message(Model):
    """
    This message model is used to represent multiple types of discord messages

    This will be linked under MESSAGE. It's important to note that this Message object might not be a normal message
    you'd expect. See :py:class:`~pycord.models.message.MessageType` for more information.

    :ivar id: The ID of the message
    :vartype id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar channel_id: The ID of the channel it was sent in
    :vartype channel_id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar guild_id: The ID of the guild it was sent in, if applicable
    :vartype guild_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar author: The user that sent the message
    :vartype author: :py:class:`~pycord.models.user.User`
    :ivar member: If the message was sent in a guild, the member that sent it
    :vartype member: Optional[:py:class:`~pycord.models.guild.Member`]
    :ivar content: The actual message that was sent
    :vartype content: str
    :ivar timestamp: An ISO8601 timestamp of when the message was posted
    :vartype timestamp: str
    :ivar timestamp_date: A parsed version of the timestamp (accuracy not ensured, use arrow or dateutil)
    :vartype timestamp_date: datetime.datetime
    :ivar edited_timestamp: When the messages was edited, None if it wasn't edited
    :vartype edited_timestamp: Optional[str]
    :ivar edited_timestamp_date: A parsed version of the edited timestamp (accuracy not ensured, use arrow or dateutil)
    :vartype edited_timestamp_date: Optional[datetime.datetime]
    :ivar tts: If True, the message is Text-To-Speech
    :vartype tts: False
    :ivar mention_everyone: If True, the message includes a @everyone
    :vartype mention_everyone: bool
    :ivar mentions: A list of people mentioned, these user objects will have the member property
    :vartype mentions: List[:py:class:`~pycord.models.user.User`]
    :ivar mention_roles: A list of snowflakes related to the roles that were mentioned in the message
    :vartype mention_roles: List[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar attachments: A list of files that were sent with the message
    :vartype attachments: List[:py:class:`~pycord.models.message.Attachment`]
    :ivar embeds: A list of embeds that were sent with the message
    :vartype embeds: List[:py:class:`~pycord.models.message.Embed`]
    :ivar reactions: A list of reactions to the message, if applicable
    :vartype reactions: List[:py:class:`~pycord.models.message.Reaction`]
    :ivar nonce: A special little snowflake (see what I did there) to confirm the message was sent
    :vartype nonce: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar pinned: If True, the message was pinned to the channel
    :vartype pinned: bool
    :ivar webhook_id: If the message was sent by a webhook, this is it's ID
    :vartype webhook_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar type: The type of message that was sent as a number
    :vartype type: int
    :ivar message_type: An enum with the type of message this is
    :vartype message_type: enum.Enum
    :ivar activity: If the message is a special message, special information
    :vartype activity: Optional[:py:class:`~pycord.models.message.MessageActivity`]
    :ivar application: If the message is a special kind of special, super special information
    :vartype application: Optional[:py:class:`~pycord.models.message.MessageApplication`]
    """
    id: pycord.config.SNOWFLAKE
    channel_id: pycord.config.SNOWFLAKE
    guild_id: Optional[pycord.config.SNOWFLAKE]
    author: pycord.config.USER
    member: Optional[pycord.config.MEMBER]
    content: str
    timestamp: str
    edited_timestamp: Optional[str]
    tts: bool
    mention_everyone: bool
    mentions: List[pycord.config.USER]
    mention_roles: List[pycord.config.SNOWFLAKE]
    attachments: List[pycord.config.ATTACHMENT]
    embeds: List[pycord.config.EMBED]
    reactions: Optional[List[pycord.config.REACTION]]
    nonce: Optional[pycord.config.SNOWFLAKE]
    pinned: bool
    webhook_id: Optional[pycord.config.SNOWFLAKE]
    type: int
    activity: Optional[pycord.config.MESSAGE_ACTIVITY]
    application: Optional[pycord.config.MESSAGE_APPLICATION]

    @property
    def message_type(self):
        for enum in MessageActivityType:
            if enum.value == self.type:
                return enum

    @property
    def timestamp_date(self):
        return parse_timestamp(self.timestamp)

    @property
    def edited_timestamp_date(self):
        return parse_timestamp(self.edited_timestamp) if self.edited_timestamp else None
