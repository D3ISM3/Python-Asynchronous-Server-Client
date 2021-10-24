import asyncio
from aioconsole import ainput


class Client:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.__reader: asyncio.StreamReader = reader
        self.__writer: asyncio.StreamWriter = writer
        self.__ip: str = writer.get_extra_info('peername')[0]
        self.__port: int = writer.get_extra_info('peername')[1]
        self.nickname: str = str(writer.get_extra_info('peername'))

    def __str__(self):
        '''
        Outputs client information as '<nickname> <ip>:<port>'
        '''
        return f"{self.nickname} {self.ip}:{self.port}"

    @property
    def reader(self):
        '''
        Gets the StreamReader associated with a client.
        '''
        return self.__reader

    @property
    def writer(self):
        '''
        Gets the StreamWriter associated with a client.
        '''
        return self.__writer

    @property
    def ip(self):
        '''
        Gets the ip associated with a client
        '''
        return self.__ip

    @property
    def port(self):
        '''
        Gets the port associated with a client
        '''
        return self.__port

    async def get_message(self):
        '''
        Retrieves the incoming message from a client and returns it in string format.
        Parameters
        ----------
        client : Client
            The client who's message will be received.
        ----------
        Returns
        -------
        str
            The incoming client's message as a string.
        -------
        '''
        return str((await self.reader.read(255)).decode('utf8'))
