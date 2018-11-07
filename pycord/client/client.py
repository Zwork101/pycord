from typing import Callable, Union

from pycord.exceptions import ReusedCommandName


class Client:
    """
    Used to represent the client program. Used for both single-file / extension styles.

    :cvar EVENT_HANDLERS: A dict with 2 keys, events and commands. Each has a dict with the corresponding name and
    :py:class:`~pycord.client.commands.Command` / :py:class:`~pycord.client.events.Event` object.
    :type EVENT_HANDLERS: {"events": Dict[str, :py:class:`~pycord.client.events.Event`], "commands": Dict[str,
    :py:class:`~pycord.client.commands.Command`]}
    :cvar config: A reference to the :py:mod:`pycord.config`
    :type config: :py:mod:`pycord.config`

    :ivar prefix: Supplied in __init__
    :type prefix: Union[Callable, str]
    :ivar commands: A dict containing command name -> :py:class:`~pycord.client.commands.Command`
    :type commands: Dict[str, :py:class:`~pycord.client.commands.Command`]
    :ivar events: A dict containing event name -> :py:class:`~pycord.client.events.Event`
    :type events: Dict[str, :py:class:`~pycord.client.commands.Command`]
    :ivar extensions: A dict containing plugin names to :py:class:`~pycord.client.extensions.Extension`
    :type extensions: Dict[str, :py:class:`~pycord.client.extensions.Extension`]
    """

    import pycord.config as config
    EVENT_HANDLERS = {"events": {}, "commands": {}}

    def __init__(self, prefix: Union[Callable, str]):
        """
        Client Setup

        :param prefix: The prefix commands will start with
        :type prefix: Union[Callable, str]
        """
        self.prefix = prefix
        self.commands = {}
        self.events = {}
        self.extensions = {}

    @classmethod
    def add_command(self, match: str, ):
        pass  # TODO: Work on this aswell
