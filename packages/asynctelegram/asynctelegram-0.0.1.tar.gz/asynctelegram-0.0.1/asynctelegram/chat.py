from .http import Http
from typing import Union

class Chat(object):

    def __init__(self, data: dict, http: Http=None):
        self.raw = data

        self.http = http

        self.id: int = data.get("id")
        self.type: str = data.get("type")
        self.title: Union[str, None] = data.get("title")
        self.username: Union[str, None] = data.get("username")
        self.first_name: Union[str, None] = data.get("first_name")
        self.last_name: Union[str, None] = data.get("last_name")

    async def send(self, text):
        return await self.http.post("sendMessage", {
            "chat_id": self.id,
            "text": text
        })