from datetime import datetime
from enum import Enum
from typing import List, Optional

import pycord.config
from .base import comboproperty, Model
from pycord.helpers import parse_timestamp


class ActivityType(Enum):
    """
    An enum with the different types of activities

    There are three different activities of discord that can be displayed. The first being games, which may include
    more information so that people can join the game. You can stream, but the URL for the activity must be a twitch
    link. Finally you can listen, which may also have extra details.

    :cvar GAME: The "Playing {game}" status
    :vartype GAME: enum.Enum
    :cvar STREAMING: The "Streaming {thing}" status
    :vartype STREAMING: enum.Enum
    :cvar LISTENING: The "Listening to {song}" status
    :vartype LISTENING: enum.Enum
    """
    GAME = 0
    STREAMING = 1
    LISTENING = 2


class ActivityTimestamps(Model):
    """
    A model that represents the times at which the activity times

    This will be linked under ACTIVITY_TIMESTAMPS. This is a small model, simply used to hold information about when
    the activity started, and when it ended.

    :ivar start: The time at which the user started this activity
    :vartype start: Optional[int]
    :ivar start_date: A parsed version of the start time
    :vartype start_date: datetime.datetime
    :ivar end: When the user stopped doing the activity
    :vartype end: Optional[int]
    :ivar end_date: A parsed version of the end time
    :vartype end_date: datetime.datetime
    """
    start: Optional[int]
    end: Optional[int]

    @comboproperty
    def start_date(self):
        return datetime.utcfromtimestamp(self.start // 1000)

    @comboproperty
    def end_date(self):
        return datetime.utcfromtimestamp(self.end // 1000)


class ActivityParty(Model):
    """
    A model that represents discord activity game parties

    This will be linked under ACTIVITY_PARTY. This model is used to hold information about the party the user is in,
    assuming they're actually in one.

    :ivar id: The ID of the party
    :vartype id: Optional[str]
    :ivar size: A list containing the min and max amount of people in the group, like [min_size, max_size]
    :vartype size: Optional[List[int]]
    """
    id: Optional[str]
    size: Optional[List[int]]


class ActivityAssets(Model):
    """
    A model that represents images for a discord activity

    This will be linked under ACTIVITY_ASSETS. This model is simply used to hold information about images.

    :ivar large_image: Usually a snowflake, but because that can't be ensured it's a string
    :vartype large_image: Optional[str]
    :ivar large_text: Text that's revealed when you hover over the large image
    :vartype large_text: Optional[str]
    :ivar small_image: Usually a snowflake, but because that can't be ensured it's a string
    :vartype small_image: Optional[str]
    :ivar small_text: Text that's revealed when you hover over the small image
    :vartype small_text: Optional[str]
    """
    large_image: Optional[str]
    large_text: Optional[str]
    small_image: Optional[str]
    small_text: Optional[str]


class ActivitySecrets(Model):
    """
    The activity model that stores secrets so people can join the game

    This will be linked under ACTIVITY_SECRETS. This model is simply used to store keys, that can be used to join the
    game.

    :ivar join: A secret used to join the game, if available
    :vartype join: Optional[str]
    :ivar spectate: A secret used to let people spectate the game
    :vartype spectate: Optional[str]
    :ivar match: Just some more secrets
    :vartype match: Optional[str]
    """
    join: Optional[str]
    spectate: Optional[str]
    match: Optional[str]


class Activity(Model):
    """
    The activity model to represent playing, watching, or listening status

    This will be linked under ACTIVITY. This model can show that someone is listening, playing, or streaming. All
    watching models use https://twitch.tv, and game objects may have info like the match if the game supports discord
    integration.

    :ivar name: The game of the activity
    :vartype name: str
    :ivar type: The type of activity (play, stream, listen)
    :vartype type: int
    :ivar message_type: A parsed version of the type
    :vartype message_type: :py:class:`~pycord.models.gateway.ActivityType`
    :ivar url: The url to the activity. For streaming, this is a twitch url
    :vartype url: Optional[str]
    :ivar timestamps: A model with information on when the activity started / ended
    :vartype timestamps: Optional[:py:class:`~pycord.models.gateway.ActivityTimestamps`]
    :ivar application_id: The ID of the app responsible for the activity
    :vartype application_id: Optional[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar details: Information about the activity
    :vartype details: Optional[str]
    :ivar state: The current status of the activity
    :vartype state: Optional[str]
    :ivar party: Information about the current party, and how to join
    :vartype party: Optional[:py:class:`~pycord.models.gateway.ActivityParty`]
    :ivar assets: IDs to images that are displayed with the activity
    :vartype assets: Optional[:py:class:`~pycord.models.gateway.ActivityAssets`]
    :ivar secrets: Keys that can be used to join, spectate, etc
    :vartype secrets: Optional[:py:class:`~pycord.models.gateway.ActivitySecrets`]
    :ivar instance: Not sure, I think if True, the activty is in progress
    :vartype instance: Optional[bool]
    :ivar flags: A bitset with information about the activity
    :vartype flags: Optional[int]
    """
    name: str
    type: int
    url: Optional[str]
    timestamps: Optional[pycord.config.ACTIVITY_TIMESTAMP]
    application_id: Optional[pycord.config.SNOWFLAKE]
    details: Optional[str]
    state: Optional[str]
    party: Optional[pycord.config.ACTIVITY_PARTY]
    assets: Optional[pycord.config.ACTIVITY_ASSETS]
    secrets: Optional[pycord.config.ACTIVITY_SECRETS]
    instance: Optional[bool]
    flags: Optional[int]

    @comboproperty
    def activity_type(self):
        for activity in ActivityType:
            if activity.value == self.type:
                return activity


class PresenceUpdate(Model):
    """
    The presence model to represent someone's current discord status

    This will be linked under PRESENCE_UPDATE. This model is used to show if someone is in a game, streaming,
    etc. It also explains if they're online or not.

    :ivar user: The user this model is for
    :vartype user: :py:class:`~pycord.models.user.User`
    :ivar roles: A list of snowflakes that represent the user's roles on the guild
    :vartype roles: List[:py:class:`~pycord.models.snowflake.Snowflake`]
    :ivar game: The user's current activity
    :vartype game: Optional[:py:class:`~pycord.models.gateway.Activity`]
    :ivar guild_id: The ID of the guild this model is for
    :vartype guild_id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar status: The current status, with be the following: "idle", "dnd", "online", or "offline"
    :vartype status: str
    :ivar activities: A list of activities the user is currently undertaking
    :vartype activities: List[:py:class:`~pycord.models.gateway.Activity`]
    """
    user: pycord.config.USER
    roles: List[pycord.config.SNOWFLAKE]
    game: Optional[pycord.config.ACTIVITY]
    guild_id: pycord.config.SNOWFLAKE
    status: str
    activities: List[pycord.config.ACTIVITY]


class ChannelPinsUpdate(Model):
    """
    The pin update model to represent when a pin is deleted to removed.

    This will be linked under CHANNEL_PINS_UPDATE. This model is used for when a pin is added, or removed. It is not
    used however when a message is deleted, that was pinned.

    :ivar channel_id: The ID of the channel the pin was in
    :vartype channel_id: :py:class:`~pycord.models.snowflake.Snowflake`
    :ivar last_pin_timestamp: # TODO: Get this model done
    """
    channel_id: pycord.config.SNOWFLAKE
    last_pin_timestamp: Optional[str]

    @property
    def last_pin_date(self):
        return parse_timestamp(self.last_pin_timestamp) if self.last_pin_timestamp else None
