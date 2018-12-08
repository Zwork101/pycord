from datetime import datetime


def parse_timestamp(timestamp: str):
    """
    Parse a timestamp returned by discord

    This is not a reliable method at all, and if you need an accurate and safe way to read properties that use this
    function, it is advised that you checkout the dateutil or arrow libraries for that.

    :param timestamp: An ISO8601 timestamp
    :type timestamp: str
    :return: A parsed datetime object with the corresponding values
    :rtype: datetime.datetime
    """
    return datetime.strptime(timestamp[:-6], "%Y-%m-%dT%H:%M:%S.%f")

def prefix(start_text: str):
    """
    Return a function that checks a message for prefix

    The returned function will check to see if it starts with the provided text. If it does, it will return an index
    for when the message actually starts. For example, if the prefix was py! and the message was py!help, it would
    return 3 because `'py!help'[3:]` is the message without the prefix, which is used by the client.

    :param start_text: The text that should act as a prefix
    :type start_text: str
    :return: A function described above
    :rtype: Callable
    """
    def checker(msg):
        if msg.content.startswith(start_text):
            return len(start_text)
    return checker

def mention_or(start_text: str):
    """
    Return index when mentioned or prefixed

    This function is exactly like :py:func:`~pycord.helpers.prefix`, however also will return with index if mentioned.

    :param start_text: The text that should act as a prefix
    :type start_text: str
    :return: A function described above
    :rtype: Callable
    """
    check_prefix = prefix(start_text)
    def checker(msg):
        if msg.content.startswith(msg.d_client.user.mention):
            return len(msg.d_client.user.mention)
        if msg.content.startswith("<@!{0}>".format(msg.d_client.user.id)):
            return len("<@!{0}>".format(msg.d_client.user.id))
        return check_prefix(start_text)
    return checker
