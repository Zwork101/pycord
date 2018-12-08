from typing import Any, Dict

import pycord.config
from pycord.gateway.codes import Opcodes
from pycord.models.message import Message


class Dispatcher:
    """
    The class that takes events returned by the gateway and gives them a home

    More specifically, this class takes all the events from the gateway, and decides what to do with them. To make your
    own, set the pycord.config.DISPATCHER var. This should do 3 similar things, get events, and look for listeners that
    want them. If it's a MESSAGE_CREATE event, hand those off to commands that match the prefix + command name. You can
    then let the Command decide if it also matches the pattern. The last task the dispatcher must manage is heartbeats,
    the gateway is relies on this reset the heartbeat_check (to make sure the server is responding) and to respond to
    the server's heartbeats too us. Set your own dispatcher under pycord.config.DISPATCHER
    """

    def __init__(self, client):
        """
        Setup the dispatcher. While you can do this later, it's advised that you load all commands and listeners here.

        :param client: The client that owns this dispatcher
        :type client: :py:class:`~pycord.client.client.Client`
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")

    def __call__(self, data: Dict[str, Any]):
        """
        Find the model related to the event, and send it to the correct command / listener. If it's a heartbeat we'll
        deal with that too.

        This is the heart and soul of the dispatcher. You must do the following things.

        1. Call .got_heartbeat() on client.gateway when you receive a heartbeat ACK (op code 11)
        2. Send a heartbeat using client.gateway.send when you receive a heartbeat (op code 1)
        3. Trigger all correct Command objects when you receive a MESSAGE_CREATE (create Message object for it)
        4. Trigger all correct Event objects when you receive any event.
        5. Pro-Tip: Discord is weird and data MAY be a list. If that's the case, just ignore it and move on

        To start a :py:class:`~pycord.client.commands.Command` or :py:class:`~pycord.client.events.Event` object, just
        call .start() on it, and pass in the Model.

        :param data: The discord payload
        :type data: Dict[str, Any]
        :return: Nothing.
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")


class AsyncDispatcher(Dispatcher):
    """
    A dispatcher build around libraries that use async / await syntax.

    Dispatches events from the gateway to the Command and Event object found from extensions. Also deals with sending /
    receiving heartbeats. Keep in mind you may have a some issues if you try to use this on a lib that's not trio, as it
     was only built with the trio lib in mind. With that said it should work with other programs such as asyncio.

    :ivar client: The client this class
    :vartype client: :py:class:`~pycord.client.client.Client`
    :ivar commands: A list of all commands that were assigned to the client
    :vartype commands: List[:py:class:`~pycord.client.commands.Command`]
    :ivar listeners: List[:py:class:`~pycord.client.events.Event`]
    """

    def __init__(self, client):
        """
        Trio gateway constructor

        Here we'll load all the commands and listeners from the extensions into lists

        :param client: The client this dispatcher belongs to
        :vartype client: :py:class:`~pycord.client.client.Client`
        """
        self.client = client
        self.commands = []
        self.listeners = []
        for extension in self.client.extensions:
            self.commands += extension._get_commands()
            self.listeners += extension._get_listeners()

        self.events = {
            "GUILD_CREATE": self.client.config.GUILD,
            "PRESENCE_UPDATE": self.client.config.PRESENCE_UPDATE,
            "MESSAGE_CREATE": self.client.config.MESSAGE
        }

    async def __call__(self, data: Dict[str, Any]):
        """
        Organize all the events we receive

        This function is used to manage all events received by the gateway. See
        :py:class:`~pycord.gateway.dispatcher.Dispatcher` for more information.

        :param data: A discord payload received by the gateway
        :type data: Dict[str, Any]
        :return: Nothing
        """
        if data['op'] == Opcodes.Heartbeat.value:
            await self.client.gateway.send(Opcodes.Heartbeat, {
                "d": self.client.gateway.sequence
            })
        elif data['op'] == Opcodes.HeartbeatACK.value:
            self.client.gateway.got_heartbeat()
        elif data['op'] == Opcodes.Reconnect.value:
            self.client.reconnect()
        elif data['op'] == Opcodes.Dispatch.value:
            if data['t'] == 'READY':
                self.client.user = self.client.config.USER(self.client, data['d']['user'])
                self.client.gateway.session_id = data['d']['session_id']
            else:
                event = self.events.get(data['t'])
                if event and data['t'] == "MESSAGE_CREATE":
                    msg = Message(self.client, data['d'])
                    for cmd, parsed_msg in self.client.get_command(msg):
                        await cmd.invoke(msg, parsed_msg)


