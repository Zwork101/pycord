from pycord.client import PycordExtentsion
from pycord.models import Message


class TestExtension(PycordExtentsion):

    @PycordExtentsion.command("ping", "*|name/str| |thing/int|")
    async def test(name: str, thing: int=None):
        print(Message.content, Message.id)
        print(name, thing)
