import os
from typing import Callable, Union

from pycord.exceptions import AuthenticationError, GatewayError


class Client:
    """
    Used to represent the client program. Used for both single-file / extension styles.

    :cvar EVENT_HANDLERS: A dict with 2 keys, events and commands. Each has a dict with the corresponding name and
    :py:class:`~pycord.client.commands.Command` / :py:class:`~pycord.client.events.Event` object.
    :vartype EVENT_HANDLERS: {"events": Dict[str, :py:class:`~pycord.client.events.Event`], "commands": Dict[str,
    :py:class:`~pycord.client.commands.Command`]}
    :cvar config: A reference to the :py:mod:`pycord.config`
    :vartype config: :py:mod:`pycord.config`

    :ivar prefix: Supplied in __init__
    :vartype prefix: Union[Callable, str]
    :ivar commands: A dict containing command name -> :py:class:`~pycord.client.commands.Command`
    :vartype commands: Dict[str, :py:class:`~pycord.client.commands.Command`]
    :ivar events: A dict containing event name -> :py:class:`~pycord.client.events.Event`
    :vartype events: Dict[str, :py:class:`~pycord.client.commands.Command`]
    :ivar extensions: A dict containing plugin names to :py:class:`~pycord.client.extensions.Extension`
    :vartype extensions: Dict[str, :py:class:`~pycord.client.extensions.Extension`]
    :ivar gateway: The client's connection to the discord gateway, setup in config
    :vartype gateway: :py:class:`~pycord.gateway.gate.Gateway`
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

        self.setup()
        self.gateway = self.config.GATEWAY(self)
        self.dispatcher = self.config.DISPATCHER(self)

        # Will be set later
        self.token: str = None
        self._presence: dict = None

    def run(self, token: str = None):
        """
        Start the bot, or really just start the gateway

        This method will call .start() on the gateway should be a blocking function. It also sets the token property
        on the client for further use. If token is not supplied then it will check the environment variables for 'TOKEN'

        :param token: The discord API token generated for the bot. If not supplied will check env variables for 'TOKEN'
        :type token: str
        :return: Nothing, as this should not end. If the bot needs to reconnect to the gateway
        """
        if not token and 'TOKEN' not in os.environ:
            raise AuthenticationError("Token not supplied and 'TOKEN' is not an environment variable")
        self.token = token or os.environ['TOKEN']
        self.gateway.start()

    def reconnect(self):
        """
        Close connection to the discord API, and then create a new one.

        This function calls .close() on the gateway, which should stop whatever thread it's on and end the connection.
        It will then check to see if the previos gateway had sequence, session_id, or _reconnect properties, and then
        pass them in as kwargs (They'll still be passed in as None if the properties don't exist). Then it

        :return: Nothing
        """
        self.gateway.close()
        kwargs = {}
        for name in ("sequence", "session_id", "_reconnect"):
            kwargs[name] = getattr(self.gateway, name, None)
        if hasattr(self.gateway, "_reconnect") and self.gateway._reconnect:
            raise GatewayError("Reconnecting too early, possible infinite gateway reconnect")
        self.gateway = self.config.GATEWAY(self, **kwargs)

    def setup(self):
        """
        Parse pycord.config's annotations and fill the file with the correct values

        Because all the discord models are spread across multiple files, you need to be careful, to prevent importing
        2 files at the same time. One way that we can get around this, is annotations. This function will go through
        all the annotated variables equal to None, and then set the value to the annotated class. Called when you
        initilize the client, so there's little need to call this yourself.

        :return: Nothing
        """
        for name, annotation in self.config.__annotations__.items():
            if not getattr(self.config, name):
                file, cls = annotation.rsplit('.', 1)
                loaded_cls = getattr(__import__(file, fromlist=[cls]), cls)
                setattr(self.config, name, loaded_cls)
