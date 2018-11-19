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
