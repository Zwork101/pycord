import pycord.config


class Extension:
    """
    Used for the extension architecture, to modularize code.

    Exceptions are like the cogs in discord.py and the Plugins in disco-py. Used to separate python code into multiple
    files for max organizational value. This class in actually quite important when importing. The client will check
    files for classes that inherit from *this class*, so you must inherit it.
    """

    @classmethod
    def _install_command(cls, name: str, pattern: str, func, *args, command=None, **kwargs):
        """
        Add command to the dict of commands

        Creates a new command object, and attach it to the function. When the extension is assigned a client,
        it will look for functions that has the 'pycord' attribute created in this function. The value should be
        some form of command object.

        :param name: The name of the command, passed into command object.
        :type name: str
        :param pattern: A pattern to match command, passed into command object.
        :param func:
        :param args:
        :param kwargs:
        :return:
        """
