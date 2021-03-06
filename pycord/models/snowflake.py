from datetime import datetime

DISCORD_EPOCH = 1420070400000


class Snowflake(int):
    """
    An object to represent a discord snowflake

    Keep in mind, that this is just a normal int with some added properties. This is the only object that doesn't
    inherit from :py:class:`~pycord.models.base.Model`. For the most part, you can just treat this like a normal int.

    :ivar increment: "For every ID that is generated on that process, this number is incremented" ~ discord docs
    :vartype increment: int
    :ivar internal_process_id: Undocumented, but supposedly the ID of the process that made the snowflake
    :vartype internal_process_id: int
    :ivar internal_worker_id: Undocumented, but supposedly the ID of the worker that made the snowflake
    :vartype internal_worker_id: int
    :ivar timestamp: A datetime object containing the point in time that the snowflake was created
    :vartype timestamp: datetime.datetime
    """

    @property
    def increment(self):
        return self & 0xFFF

    @property
    def internal_process_id(self):
        return (self & 0x1F000) >> 12

    @property
    def internal_worker_id(self):
        return (self & 0x3E0000) >> 17

    @property
    def timestamp(self):
        return datetime.utcfromtimestamp(((self >> 22) + DISCORD_EPOCH) / 1000)

    def is_valid(self):
        """
        Complete a series of checks to see if it could be a snowflake

        The following checks are to ensure that it *could* be a discord ID.
        1. Makes sure it isn't 0 or less
        2. It makes sure the snowflake isn't larger than 64 bits.
        3. It makes sure the snowflake is at least 22 bits.
        2. It makes sure the timestamp isn't less than the discord epoch.
        3. It makes sure the timestamp isn't greater than now

        :return: True if the ID could belong to discord, False otherwise.
        :rtype: bool
        """
        if self <= 0:
            return False
        elif 22 > self.bit_length() > 64:
            return False
        elif self.timestamp < datetime.utcfromtimestamp(DISCORD_EPOCH / 1000):
            return False
        elif self.timestamp > datetime.now():
            return False
        return True
