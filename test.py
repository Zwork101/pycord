from pycord.gateway.gate import TrioGateway


class Client:

    def __init__(self):
        self.token = "NDQwMzE0NDExNDkyNzA0Mjg3.DspYGQ.sQfP5LAc1mZdNARaHpzO9iPVbAc"
        self._presence = None

    def reconnect(self):
        print("tried to reconnect")

    async def dispatcher(self, data):
        print("Got: ", data)


gateway = TrioGateway(Client())
gateway.start()
