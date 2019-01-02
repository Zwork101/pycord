from pycord.client import PycordExtentsion
from pycord.models import Message, User, PremiumTypes


class TestExtension(PycordExtentsion):

    @PycordExtentsion.command("ping", "*|name/str| |thing/int|")
    async def test(name: str, thing: int=None):
        print(Message.content, Message.id, Message.message_type)
        print(User.premium_type)
        print(User.name, User.has(PremiumTypes.NITRO))
        print(name, thing)
