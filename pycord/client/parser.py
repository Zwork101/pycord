from itertools import count
from typing import Any, List
import re

from pycord.exceptions import ParseError, CannotCastTypes


class Parser:
    """
    A class to outline how a parser should act.

    Parsers are objects used to determine if someone invoked a command. For example, The ReParser might do
    "kick (?P<user>\d+)" which would match (assuming the prefix is `?`) something like this:

        ?kick 12356789

    """

    def __init__(self, selector: Any):
        """
        The __init__ function will be passed in a value, which it will match up against

        :param selector: The value which will be compared to the command text (without prefix)
        :type selector: Any
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")

    def match(self, text: str):
        """
        Match the text, if it does match, return a object for :py:meth:`~pycord.client.parser.Parser.load`

        If the match failed, make sure you return None, and load won't be called. It's very important that
        you do not try to send a None value to load.

        :param text: The text a user wrote that started with a prefix (prefix excluded)
        :type text: str
        :return: A value to be passed into :py:meth:`~pycord.client.parser.Parser.load`
        :rtype: Any
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")

    def load(self, *args, **kwargs):
        """
        Load the result of :py:meth:`~pycord.client.parser.Parser.match` to get arguments for command execution.

        If load returns "None", the function will not be called. On the other hand, if you're casting types, you
        should raise a :py:exc:`~pycord.exceptions.CannotCastTypes`, and have the first argument be a dict. At least,
        the dict should return something like this:

          {"name": "foo", "value": "bar", "type": "int"}

        However feel free to add more to the list, if you know other plugins can use those values.


        :param args: Should be changed depending on requirements
        :param kwargs: Should be changed depending on requirements
        :return: A tuple conating a list of args, and a dict of kwargs
        :rtype: Union[Tuple[List[Any], Dict[str, Any]], None]
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")


class ReParser(Parser):
    """
    A regex command parser

    :ivar compiled: Compiled regex, based on the regex passed in.
    :vartype compiled: Regular Expression Object
    """

    def __init__(self, regex: str):
        self.compiled = re.compile(regex)

    def match(self, text: str):
        """
        Attempt to match text to regex

        :param text: Text from message excluding prefix
        :type text: str
        :return: Either None or a regex match object
        :rtype: Union[None, re.Match]
        """
        return self.compiled.match(text)

    def load(self, re_match: "re.Match"):
        """
        Load args and kwargs from regex Match

        args are determined from the groups that don't have names. Groups that use (?P<name>) will be kwargs.

        :param re_match: A match returned from matching sequence.
        :type re_match: re.Match
        :return: A tuple with a list of either strings or None, and a dict with strings to either more strings or None.
        :rtype: Union[Tuple[List[Union[str, None]], Dict[str, Union[str, None]]], None]
        """

        args = []
        kwargs = re_match.groupdict()
        kwarg_positions = [re_match.span(g) for g in kwargs]
        for i, arg in enumerate(re_match.groups()):
            if re_match.span(i) not in kwarg_positions:
                args.append(arg)

        return args, kwargs


def yes_no(text: str):
    """
    Helper function to determine yes / no value

    WARNING: This really only works with english servers.
    """
    return True if text[0].lower() == "y" else False


class PycordParser(Parser):
    """
    Custom pycord parser, similar to disco-py

    | The syntax is as follows. * Makes a block required, | starts and ends blocks, / is to differ from a block's name a
    nd type, and ; is used to escape any of the previously mentioned characters. Examples of such matchings are:

    | `*|mention/str| |time/int|`
    | `*|num1/float| ;* *|num2/float|`

    You can add types to the class through :py:attr:`~pycord.client.parser.PycordParser.TYPES`, however the default ones
    are str, int, float, and yn. 'yn' returns a bool, depending on whether the block started with 'y' or 'Y'.

    :cvar TYPES: A dict containing type names to a corresponding callable object that returns instances.
    :vartype TYPES: Dict[str, Callable]

    :ivar checks: A list of strings or lists used to matching and loading.
    :vartype checks: List[Union[str, List[bool, str, str]]
    """

    TYPES = {
        "str": str,
        "int": int,
        "float": float,
        "yn": yes_no
    }

    def __init__(self, selector: str):
        """
        Setup PycordParser

        :param selector: A string to represent what will be matched. See class docs for more information.
        :type selector: str
        """
        self.checks = [""]
        inside_check = False
        check_index = None

        chars = iter(zip(count(), selector))
        for i, char in chars:
            if char == "*" and not inside_check:
                try:
                    i, next_char = next(chars)
                except StopIteration:
                    raise ParseError("Unexpected '*' requirement at end of string. Did you mean to escape it with ';'?")
                if next_char == "|":
                    inside_check = True
                    self.checks.append([True, "", ""])
                    check_index = 1
                else:
                    raise ParseError("Expected new check with '|' at column {0}".format(i))
            elif char == "*" and inside_check:
                raise ParseError("Unexpected '*' requirement at column {0}. Did you mean to escape it with ';'?"
                                 .format(i))
            elif char == "|" and not inside_check:
                inside_check = True
                self.checks.append([False, "", ""])
                check_index = 1
            elif char == "|" and inside_check:
                if check_index == 2:
                    inside_check = False
                    self.checks.append("")
                else:
                    raise ParseError("Unexpected '|' block start at column {0}. Did you mean to escape it with ';'?"
                                     .format(i))
            elif char == "/" and inside_check:
                if check_index == 2:
                    raise ParseError("Only one '/' allowed in block at column {0}. Did you mean to escape it with ';'?"
                                     .format(i))
                check_index += 1
            elif char == "/" and not inside_check:
                raise ParseError("Unexpected block shift at column {0}. Did you mean to escape it with ';'?"
                                 .format(i))
            elif char == ";":
                try:
                    _, next_char = next(chars)
                except StopIteration:
                    raise ParseError("Unexpected escape at end of string. Did you mean to escape with ';'?")
                if isinstance(self.checks[-1], list):
                    self.checks[-1][check_index] += next_char
                else:
                    self.checks[-1] += next_char
            else:
                if isinstance(self.checks[-1], list):
                    self.checks[-1][check_index] += char
                else:
                    self.checks[-1] += char

        if self.checks and not self.checks[0]:
            self.checks = self.checks[1:]
        if self.checks and not self.checks[-1]:
            self.checks = self.checks[:-1]

        if not self.checks:
            return  # In this case, the command would trigger with just saying the prefix

        check_iter = iter(self.checks)
        for i, check in enumerate(check_iter):
            if isinstance(check, list):
                try:
                    if not isinstance(next(check_iter), str):
                        raise ParseError("You must separate blocks.")
                except StopIteration:
                    pass

        if set(c[1] for c in self.checks if isinstance(c, list))\
                .difference(c[1] for c in self.checks if isinstance(c, list)):
            raise ParseError("There can not be multiple blocks with the same name")

        invalid_checks = [c for c in self.checks if isinstance(c, list) and c[2] not in self.TYPES]
        if invalid_checks:
            raise ParseError("Unknown types used: {0}".format(','.join(invalid_checks)))

        required_max_index = max([self.checks.index(b) for b in self.checks if isinstance(b, list) and b[0]] or [-1])
        unrequired_min_index = min([self.checks.index(b) for b in self.checks if isinstance(b, list) and not b[0]]
                                   or [-1])
        if required_max_index > unrequired_min_index and required_max_index != -1 and unrequired_min_index != -1:
            raise ParseError("All required blocks must be before unrequired blocks")

    def match(self, text: str):
        """
        Attempt to match command with self.checks, which is created in
        :py:meth:`~pycord.client.parser.PycordParser.__init__`.

        :param text: Text from message excluding prefix
        :type text: str
        :return: A list of strings within the same placement as self.checks
        :rtype: Union[None, List[str]]
        """
        if not self.checks:
            return []
        if len(self.checks) == 1:
            return [] if self.checks[0] == text else None

        results = []
        for part in [s for s in self.checks if isinstance(s, str)]:
            index = text.find(part)
            if index == -1:
                results.append(text)
                break
            result, text = text[:index], text[index + len(part):]
            results.append(result)
        else:
            results.append(text)

        if isinstance(self.checks[0], str):
            results = results[1:]
        if isinstance(self.checks[-1], str):
            results = results[:1]

        if len(results) < len([c for c in self.checks if isinstance(c, list) and c[0]]):
            return
        return results

    def load(self, results: List[str]):
        """
        Get each type from the corresponding check and return kwargs.

        :param results: A list of values to be parsed
        :type results: List[str]
        :return: A tuple with an empty list, then a dict with strings to anything.
        :rtype: Tuple[List[Nothing], Dict[str, Any]]
        """
        loaded = {}
        for result, check in zip(results, [c for c in self.checks if isinstance(c, list)]):
            try:
                loaded[check[1]] = self.TYPES[check[2]](result)
            except ValueError:
                raise CannotCastTypes({"name": check[1], "value": result, "type": check[2]})
        return [], loaded
