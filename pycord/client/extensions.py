from typing import Any
from types import FunctionType

import pycord.config


class Extension:
    """
    Used for the extension architecture, to modularize code.

    Exceptions are like the cogs in discord.py and the Plugins in disco-py. Used to separate python code into multiple
    files for max organizational value. This class in actually quite important when importing. The client will check
    files for classes that inherit from *this class*, so you must inherit it.
    """

    @classmethod
    def command(cls, name: str, pattern: Any = None, **kwargs):
        """
        This classmethod (or static method or whatever, but usually Extensions are not instances) creates commands.

        The purpose of this function is to assign a create a Command object attached to the function. The Command object
        returned MUST be pycord.config.COMMAND. Usually, commands will look like this:

            class MyExtension(Extension):

                @Extension.command("help", "|page/int|")
                def show_help(self):
                  ...

        Ultimately, the arguments are up to you, however you should always ask for kwargs, which will then be supplied
        for the Command object.

        :param name: The name of the command
        :type name: str
        :param pattern: A pattern that will be matched against the text
        :type pattern: Any
        :param kwargs: Kwargs that should be passed into the Command object
        :return: A function to decorate the command
        :rtype: FunctionType
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")

    @classmethod
    def listen(cls, name: str, **kwargs):
        """
        This classmethod (or static method or whatever, but usually Extensions are not instances) creates events.

        The purpose of this command is to assign an event object with a function. This event object MUST be found in
        the pycord.config file under pycord.config.EVENT. Usually, listeners will look like:

            class MyExtension(Extension):

                Extension.listen("MESSAGE_DELETE")
                def on_message_delete(self):
                  ...

        The arguments really are up to you, however you should always accept a **kwargs. Whatever was supplied in kwargs
        should then be passed on to the event.

        :param name: Name of the event
        :type name: str
        :param kwargs: Key word arguments that should be passed into the Event
        :return: A function to decorate the listener
        :rtype: FunctionType
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")

    @classmethod
    def _get_commands(cls):
        """
        Return a list of all commands attached to the class

        This should take all the Command objects created from :py:meth:`~pycord.client.extensions.Extension.command` and
        return a list with each Command inside it.

        :return: A list of all commands attached to the extension
        :rtype: List[:py:class:`~pycord.client.commands.Command`]
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")

    @classmethod
    def _get_listeners(cls):
        """
        Return a list of all commands attached to the class

        It's the same as :py:meth:`~pycord.client.extensions.Extension._get_commands` but returns all the Events from
        :py:meth:`~pycord.client.extensions.Extension.listen`.

        :return A list of all listeners attached to the extension
        :rtype: List[:py:class:`~pycord.client.events.Event`]
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")


class PycordExtentsion(Extension):
    """
    The default PyCord Extension class, very, very simple.

    This class is used to help the client identify listeners and commands.
    """

    @classmethod
    def command(cls, name: str, pattern: Any = None, **kwargs):
        """
        Identifies the function as a command and creates a Command object for it.

        This functions adds a _pycord attribute to the function. This attribute is a dict with the type of func and
        details such as the Command object. The Command obj is from pycord.config.COMMAND. All arguments are what will
        be passed into the Command object.

        :param name: The name of the command.
        :type name: str
        :param pattern: Pattern to collect more of the invoked command.
        :type pattern: Any
        :param kwargs: Extra information passed into the Command object.
        :return: A function to, to decorate the command
        :rtype: FunctionType
        """
        cmd = pycord.config.COMMAND(name, pattern, **kwargs)

        def func_wrapper(func):
            func._pycord = {
                "type": "command",
                "data": cmd
            }
            return func
        return func_wrapper

    @classmethod
    def listen(cls, name: str, **kwargs):
        """
        Identifies the function as a listener and creates an Event for it.

        This function does the same exact thing as :py:meth:`~pycord.client.extensions.PycordExtension.command`, however
         the type specified in _pycord is "event" and the data is pycord.config.EVENT.

        :param name: The name of the event to listen to.
        :type name: str
        :param kwargs: Extra arguments to pass into the Event
        :return: A function, to decorate the listener
        :rtype: FunctionType
        """
        listener = pycord.config.EVENT(name, **kwargs)

        def func_wrapper(func):
            func._pycord = {
                "type": "event",
                "data": listener
            }
            return func
        return func_wrapper

    @classmethod
    def _get_commands(cls):
        commands = []
        for _, value in cls.__dict__.items():
            if isinstance(value, FunctionType) and hasattr(value, "_pycord"):
                if value._pycord["type"] == "command":
                    commands.append(value._pycord['data'])
        return commands

    @classmethod
    def _get_listeners(cls):
        listeners = []
        for _, value in cls.__dict__.items():
            if isinstance(value, FunctionType) and hasattr(value, "_pycord"):
                if value._pycord["type"] == "event":
                    listeners.append(value._pycord['data'])
        return listeners
