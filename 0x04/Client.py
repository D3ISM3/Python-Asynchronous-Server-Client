import asyncio
import sys
from aioconsole import ainput


class Client:
    def __init__(self, server_ip: str, server_port: int, loop: asyncio.AbstractEventLoop):
        self.__server_ip: str = server_ip
        self.__server_port: int = server_port
        self.__loop: asyncio.AbstractEventLoop = loop
        self.__reader: asyncio.StreamReader = None
        self.__writer: asyncio.StreamWriter = None

    @property
    def server_ip(self):
        return self.__server_ip

    @property
    def server_port(self):
        return self.__server_port

    @property
    def loop(self):
        return self.__loop

    @property
    def reader(self):
        return self.__reader

    @property
    def writer(self):
        return self.__writer

    async def connect_to_server(self):
        '''
        Connects to the chat server using the server_ip and server_port
        provided during initialization

        This function will also set the reader/writer properties
        upon successful connection to server
        '''
        try:
            self.__reader, self.__writer = await asyncio.open_connection(
                self.server_ip, self.server_port)
            await asyncio.gather(
                self.receive_messages(),
                self.start_client_cli()
            )
        except Exception as ex:
            print("An error has occurred: " + ex)

        print("Shutting down")

    async def receive_messages(self):
        '''
        Asynchronously receives incoming messages from the
        server.
        '''
        server_message: str = None
        while server_message != 'quit':
            server_message = await self.get_server_message()
            print(f"{server_message}")

        if self.loop.is_running():
            self.loop.stop()

    async def get_server_message(self):
        '''
        Awaits for messages to be received from self.
        If message is received, returns result as utf8 decoded string
        '''
        return str((await self.reader.read(255)).decode('utf8'))

    async def start_client_cli(self):
        '''
        Starts the client's command line interface for the user.
        Accepts and forwards user input to the connected server.
        '''
        client_message: str = None
        while client_message != 'quit':
            client_message = await ainput("")
            self.writer.write(client_message.encode('utf8'))
            await self.writer.drain()

        if self.loop.is_running():
            self.loop.stop()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} SERVER_IP PORT")

    loop = asyncio.get_event_loop()
    client = Client(sys.argv[1], sys.argv[2], loop)
    asyncio.run(client.connect_to_server())
