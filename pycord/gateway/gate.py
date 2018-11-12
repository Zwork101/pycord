from random import randint
import json
from platform import system
from typing import List, Union
from zlib import decompressobj

from pycord.exceptions import GatewayError, AuthenticationError
from pycord.gateway.codes import Opcodes

import trio
import trio_websockets


class Gateway:
    """
    The gateway that connects to discord to collect all sorts of events.

    If your plugin wants to make it's own gateway, just specify GATEWAY in the config file. If you wish to make your own
     gateway, all it requires is a start method. This method should be blocking but stops when you disconnect from the
     gateway. The instance variables listed are required and are explained in more detail in the constructor.

     :ivar sequence: This is used for reconnecting, used by client.
     :type sequence: int
     :ivar session_id: This is used for reconnecting, used by client.
     :type session_id: str
     :ivar _reconnect: This is used for reconnecting, used by client.
     :type _reconnect: bool
    """

    def __init__(self, client, sequence: int = None, session_id: str = None, _reconnect: bool = False):
        """
        The constructor for gateway objects.

        It's advised that you see TrioGateway's :py:meth:`~pycord.gatewate.gateway.TrioGateway.__init__` for more
        information, however all to put it simply, client will always be supplied, and if the client is reconnecting
        then the gateway must have previously set a sequence and session_id property. If these properties are not set,
        an error WILL NOT be raised, and None will be passed in. _reconnect is the same deal, and is just to help you
        make sure your gateway doesn't try to reconnect a bunch of times really quickly.
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")

    def start(self):
        """
        The method to start the gateway's connection and dispatch events.

        This method is used to start the gateway, to be specific, the gateway much connect and do a normal discord
        handshake. After doing so, if the connection is new, it should specify the sequence and session_id properties so
        those values can be passed into a new gateway class when reconnecting. After this, continue to listen for events
        , and when received, pass them onto the client's dispatcher (:py:attr:`~pycord.client.client.Client.dispatcher`)
        . For example,

            event = self.get_next_event()  # Just a random method which returns a discord event dict
            self.client.dispatcher(event)

        :return: Nothing, as this is a blocking function that ideally doesn't end.
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")

    def close(self):
        """
        This method ends the connection with discord's gateway.

        This method is most commonly used for reconnecting. With that said, if the socket dies and this method is called
        , you should be ready to close an already closed socket.

        :return: Nothing
        """
        raise NotImplementedError("This class needs to be inherited and overwritten using this outline.")


class TrioGateway(Gateway):
    """
    The gateway that connects to discord to collect all sorts of events using trio.

    Not really sure what else to say, it uses the trio_websockets lib which is new but suits our purposes.

    :cvar VERSION: The version of the gateway we'll be using (6 at the time of writing this)
    :type VERSION: int
    :cvar ZLIB_SUFFIX: We'll be using zlib to compress data, which needs a suffix to end a stream
    :type ZLIB_SUFFIX: str
    :cvar ENCODING: The type of encoding (We'll be using json)
    :type ENCODING: str
    :cvar COMPRESS: The type of compression used (We're using zlib-stream)
    :type COMPRESS: str

    :ivar client: The client this gateway belongs too
    :type client: :py:class:`~pycord.client.client.Client`
    :ivar buffer: A bytearray that will be used for decompressing data
    :type buffer: bytearray
    :ivar deflator: A decompressor from the builtin zlib module
    :type deflator: Whatever zlib.decompressobj() returns
    :ivar heartbeat_interval: The rate in ms that we ping the gateway, None until received by gateway.
    :type heartbeat_interval: int
    :ivar _trace: No clue what it is but discord supplies it on a HELLO event.
    :type _trace: List[str]
    :ivar sequence: The number received from the last dispatch. Can be replaced in kwargs for resuming.
    :type sequence: int
    :ivar session_id: The session ID returned from the Ready event. Can be replaced in kwargs for resuming.
    :type session_id: str
    :ivar identity: A dict that should be sent with the Identify event, contains a bunch of information.
    :type identity: Dict[str, Any]
    """

    VERSION = 6
    ZLIB_SUFFIX = b'\x00\x00\xff\xff'
    ENCODING = 'json'
    COMPRESS = "zlib-stream"

    def __init__(self, client, sequence: int = None, session_id: str = None, _reconnect: bool = False):
        """
        Constructing the gateway connection

        If you're making your own gateway class in your plugin, each of these args and kwargs are required, and will be
        passed in. If for some reason your program needs to create a Gateway object itself, it's advised that you let
        the client handle _reconnect.

        :param client: The client a this gateway belongs to
        :type client: :py:class:`~pycord.client.client.Client`
        :param sequence: If reconnecting, this is the sequence we last received.
        :type sequence: int
        :param session_id: If reconnecting, this is what we got after identifying.
        :type session_id: str
        :param _reconnect: This is to make sure something doesn't go wrong, and we don't try to reconnect hundreds of
        times.
        :type _reconnect: bool
        """
        self.client = client

        self.buffer = bytearray()
        self.deflator = decompressobj()

        # Will be set by discord API later
        self.heartbeat_interval: int = None
        self._trace: List[str] = None
        self.sequence: int = sequence
        self.session_id: str = session_id

        self._reconnect = _reconnect
        self._got_heartbeat = True
        self._closed = False
        self._send_heartbeat, self._receive_heartbeat = trio.open_memory_channel(1)
        self._conn: trio_websockets.WebSocketClientProtocol = None

    @property
    def identity(self):
        ide = {
            "token": self.client.token,
            "properties": {
                "$os": system(),
                "$browser": "pycord",
                "$device": "pycord"
            },
            "compress": bool(self.COMPRESS),
            "large_threshold": 250,
            "shard": [0, 1],
        }
        if self.client._presence:
            ide["presence"] = self.client._presence
        return ide

    @classmethod
    def gateway_url(cls):
        return "wss://gateway.discord.gg/?v={version}&encoding={encoding}&compress={compress}".format(
            version=cls.VERSION, encoding=cls.ENCODING, compress=cls.COMPRESS
        )

    @staticmethod
    def build_payload(op: Opcodes, data: Union[dict, int]):
        """
        Build a encoded json string with the supplied information.

        :param op: Opcode that's being sent
        :type op: :py:class:`~pycord.gateway.codes.Opcodes`
        :param data: Information being sent, usually a dict, except on heartbeats
        :type data: Union[dict, int]
        :return: The encoded string with json information
        :rtype: bytes
        """
        return json.dumps({
            "op": op.value,
            "d": data
        }).encode()

    async def heartbeat(self, conn: trio_websockets.WebSocketClientProtocol = None):
        """
        Send heartbeats to the server to confirm it's active

        This is a recursive function, it will continue to call itself while the connection is active. If it does not
        receive a heartbeat, it will reconnect to discord.

        :param conn: A connection to the discord gateway. Should be created by this instance.
        :type conn: trio_websockets.WebSocketClientProtocol
        :return: Nothing. This function should not end unless the connection dies.
        """
        if conn is None:
            conn = await self._receive_heartbeat.receive()
        await trio.sleep(self.heartbeat_interval // 1000)
        if not self._got_heartbeat:
            if not self._closed:
                self.client.reconnect()
        else:
            self._got_heartbeat = False
            await conn.send(self.build_payload(Opcodes.Heartbeat, self.sequence))
        if not conn.closed:
            await self.heartbeat(conn)

    async def get_message(self, conn: trio_websockets.WebSocketClientProtocol):
        """
        Fetch for the next message sent by the server.

        This command will block until it receives enough information from the server to construct a valid json
        payload. Once it does that it will reset the buffer and return it.

        :param conn: The connection to the discord gateway
        :type conn: trio_websockets.WebSocketClientProtocol
        :return: The json payload
        :rtype: Dict[str, Any]
        """
        while True:
            try:
                msg = await conn.recv()
            except trio.ClosedResourceError:
                return
            self.buffer.extend(msg)
            if len(msg) < 4 or msg[-4:] != self.ZLIB_SUFFIX:
                continue
            loaded = json.loads(self.deflator.decompress(self.buffer).decode())
            self.buffer = bytearray()
            return loaded

    async def run(self):
        """
        This is the heart and soul of the gateway, what makes everything go.

        The order at much things happen occurs like this. We connect and then recv a message. This should be a Hello msg
        , and we get the heartbeat interval and _trace from it. After that we start a heartbeat send a identify, however
         if we disconnected and are trying to resume, we'll send a Resume, and if that fails we'll send an identify.

        :return: Nothing, hopefully won't return ever
        """
        async with trio_websockets.connect(self.gateway_url()) as conn:
            msg = await self.get_message(conn)
            if Opcodes.Hello.value != msg["op"]:
                raise GatewayError("Discord did not start with HELLO payload")
            self.heartbeat_interval = msg["d"]["heartbeat_interval"]
            self._trace = msg["d"]["_trace"]

            await self._send_heartbeat.send(conn)

            while True:
                if self.sequence and self.session_id:
                    await conn.send(self.build_payload(Opcodes.Resume, {
                        "token": self.client.token,
                        "session_id": self.session_id,
                        "sequence": self.sequence
                    }))

                    next_msg = await self.get_message(conn)
                    if next_msg["op"] == Opcodes.InvalidSession.value:
                        self.sequence, self.session_id = None, None
                        await trio.sleep(randint(1, 5))
                        continue
                    print(next_msg)
                    self._trace = next_msg['d']['_trace']
                else:
                    await conn.send(self.build_payload(Opcodes.Identify, self.identity))
                    ready_msg = await self.get_message(conn)
                    self.session_id = ready_msg['d']['session_id']
                    self._trace = ready_msg['d']['_trace']
                    self.client.dispatcher(ready_msg)
                    break

            self._reconnect = False
            self._conn = conn
            while not self._closed and not conn.closed:
                msg = await self.get_message(conn)
                if not msg:
                    break
                self.client.dispatcher(msg)

        close_code = conn.ws_client.close_code
        if close_code in (4000, 4007, 4009):
            self.client.reconnect()
        elif close_code == 4004:
            raise AuthenticationError("Invalid token")
        elif close_code != 1000:
            raise GatewayError("Unexpected error occurred: {0}".format(close_code))

    async def _start(self):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.run)
            nursery.start_soon(self.heartbeat)

    def start(self):
        """
        Start the gateway to start receiving discord events

        This function is blocking, and will block until we lose connection to the discord gateway.

        :return: Idealy this won't return at all, however discord isn't perfect. The client should usually restart if
        this ends.
        """
        trio.run(self._start)

    def close(self):
        """
        Close the gateway connection and stop the worker dispatching events.

        It's very important that this function is run after the handshake. It's hard to tell when the handshake is comp
        lete, but a good rule of thumb is to check when events start rolling in. Trying to close before a good connect
        ion is established will raise an error. You can also just wait 2-4 seconds after starting.

        :return: Nothing
        """
        if self._conn is None:
            raise GatewayError("You tried to close the gateway connection before it was established.")
        self._conn.close(1000)
        self._closed = True
