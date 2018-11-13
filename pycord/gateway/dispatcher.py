from typing import Dict, Any


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
        3. Trigger all correct Command objects when you receive a MESSAGE_CREATE
        4. Trigger all correct Event objects when you receive any event.
        5. Pro-Tip: Discord is weird and data MAY be a list. If that's the case, just ignore it and move on

        To start a :py:class:`~pycord.client.commands.Command` or :py:class:`~pycord.client.events.Event` object, just
        call .start() on it, and pass in the Model.

        :param data: The discord payload
        :type data: Dict[str, Any]
        :return: Nothing.
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")


class TrioDispatcher:
    """
    A dispatcher build around the Trio library.

    Dispatches events from the gateway to the Command and Event object found from extensions. Also deals with sending /
    receiving heartbeats.

    :ivar client: The client this class
    """
