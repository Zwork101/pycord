from typing import Any, Callable, Dict

from pycord.models.channel import Channel as ChannelModel

_CHANNEL_EVENT = {
    "Channel": {
        "complete": True,
        "data": ""
    },
    "Guild": {
        "complete": False,
        "data": "guild_id"
    }
}


EVENTS = {
    "CHANNEL_CREATE": _CHANNEL_EVENT.copy(),
    "CHANNEL_UPDATE": _CHANNEL_EVENT.copy(),
    "CHANNEL_DELETE": _CHANNEL_EVENT.copy(),
    ""
}