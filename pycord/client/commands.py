from typing import Any, Callable

import pycord.config
from pycord.exceptions import CannotCastTypes

class Command:
    """
    A object used to represent commands the bot listens too

    This object is created when you do Extention.command on a function. This class's job is too make sure that all
    appropriate context is set. In this case, the event proxy should be set to something like

        {
            "client": <client object>,
            "Message": {
                "complete": True,
                "data": <Message object>
            },
            "Channel": {
                "complete": False,
                "data": ["123456789"]
            }
        }

    For more information, see how contexts work behind the scenes, or look at the source for PycordCommand.

    :ivar name: The name of the command (used by the dispatcher)
    :vartype name: str
    """

    def __init__(self, callback: Callable, name: str, pattern: Any=None, **kwargs):
        """
        The constructor for command

        There are only 2 essential arguments, name, the name of the command and is usually used when checking if the
        command was invoked, and pattern, which is for extra information. Usually, the if I were to create a command
        like, `Command("hello", "<user>")`, the discord equivalent would look like !hello user. (Or whatever prefix
        your bot will be using)

        :param callback: The function that will be called when the command is invoked
        :type callback: Callable
        :param name: The name of the command
        :type name: str
        :param pattern: A pattern wich will be used to determine if the command was provided correct arguments
        :type pattern: Any
        :param kwargs: Any extra arguments which can be used for your own plugins
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")

    def invoke(self, msg: "pycord.models.message.Message", parsed_cmd: str):
        """
        If the data provided matches the command's pattern, call callback

        Along with calling the provided callback on initialization, this is where you set the context
        :py:var:`~pycord.config.event`. See class description for some more details

        :param msg: The message sent, that's been stripped of the prefix + command name by the dispatcher
        :type msg: :py:class:`~pycord.models.message.Message`
        :param parsed_cmd: A version of the sg.content that's had the prefix and command name removed
        :type parsed_cmd: str
        :return: Nothing
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")


class PycordCommand(Command):
    """
    The pycord object for managing commands

    This is the default object object that pycord uses to hold information about commands, it also works with setting
    up the context.

    :ivar callback: The function provided on initialization
    :vartype callback: Callable
    :ivar name: The name of the command
    :vartype name: str
    :ivar pattern: An initialized command parser, of None if no pattern was supplied
    :vartype pattern: Optional[:py:class:`~pycord.client.parser.PycordParser`]
    """

    def __init__(self, callback: Callable, name: str, pattern: str=None, parser: "pycord.client.parser.Parser"=None):
        """
        The PycordCommand constructor method

        :param callback: A function that will be called when the command is triggered, and passed in the args from the
        parser.
        :type callback: Callable
        :param name: The name of the function
        :type name: str
        :param pattern: The pattern that will be used by the parser to pass in the arguments, if you want to use one
        :type pattern: Optional[str]
        :param parser: The parser that will be used to parse the arguments, if you don't like the default
        :type parser: Optional[:py:class:`~pycord.client.parser.PycordParser`]
        """
        self.callback = callback
        self.name = name
        if pattern is not None:
            self.pattern = parser(pattern) if parser else pycord.config.COMMAND_PARSER(pattern)
        else:
            self.pattern = None

    def _make_context(self, msg: "pycord.models.message.Message"):
        ctx = {
            "client": msg.d_client,
            "Message": {
                "complete": True,
                "data": msg
            },
            "Guild": {
                "complete": False,
                "data": [msg.guild_id]
            },
            "Channel": {
                "complete": False,
                "data": [msg.channel_id]
            },
            "User": {
                "complete": True,
                "data": msg.author
            },
            "Member": {
                "complete": True,
                "data": msg.member
            },
            "Webhook": {
                "complete": False,
                "data": [msg.webhook_id]
            }
        }
        pycord.config.event.set(ctx)

    async def invoke(self, msg: "pycord.models.message.Message", parsed_cmd: str):
        if self.pattern:
            match = self.pattern.match(parsed_cmd)
            if match is not None:
                try:
                    loaded = self.pattern.load(match)
                except CannotCastTypes:
                    pass  # TODO: Do something with this so the bot knows a user sent the command wrong
                else:
                    if loaded is not None:
                        self._make_context(msg)
                        await self.callback(*loaded[0], **loaded[1])
        else:
            self._make_context(msg)
            await self.callback()
