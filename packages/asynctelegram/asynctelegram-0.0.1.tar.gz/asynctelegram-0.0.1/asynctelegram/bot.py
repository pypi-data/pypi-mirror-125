import asyncio 
from typing import Union

from .http import Http
from .user import User
from .message import Message
from .command import Command

class Bot(object):

    def __init__(self):
        self.commands = []

    async def on_login(self):
        pass

    async def on_message(self, message: Message):
        pass

    async def on_raw_event(self, event: dict):
        pass

    def stop(self):
        self.__stop = True

    def get_public_commends(self):
        for command in self.commands:
            if not command.hidden:
                yield command

    def command(self, name: Union[str, None]=None, description: str="no description", hide: bool=False):

        def decorator(func):

            self.commands.append(Command(
                func,
                name if name is not None else func.__name__,
                description,
                hide
            ))

            return func

        return decorator

    async def fetch_task(self):
        update_offset = 0
        while not self.__stop:
            updates = await self.http.get("getUpdates", data={"offset": update_offset+1})

            for update in updates:
                
                asyncio.create_task(self.on_raw_event(update))

                if update_offset < update["update_id"]:
                    update_offset = update["update_id"]

                if update.get("message"):
                    msg = Message(update.get("message"), http=self.http)
                    asyncio.create_task(self.on_message(msg))

                    for command in self.commands:
                        if msg.text is not None and len(msg.text.split()) and msg.text.split()[0] == "/"+command.name:
                            command.execute(msg)

    async def __start(self, token: str):
        self.http = Http(token)

        self.user = User(await self.http.get("getMe"), http=self.http)

        await self.on_login()

        await self.http.post("deleteMyCommands")
        await self.http.post("setMyCommands", {
            "commands": [command.to_botcommand() for command in self.get_public_commends()]
        })

        self.__stop = False
        await self.fetch_task()
        await self.http.close()

    def start(self, token: str):
        asyncio.run(self.__start(token))