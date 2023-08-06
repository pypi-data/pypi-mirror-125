from .message import Message

class Context(object):
    def __init__(self, message: Message):
        self.message = message
        self.chat = message.chat
        self.author = message.author

    async def send(self, *args, **kwargs):
        return await self.message.chat.send(*args, **kwargs)