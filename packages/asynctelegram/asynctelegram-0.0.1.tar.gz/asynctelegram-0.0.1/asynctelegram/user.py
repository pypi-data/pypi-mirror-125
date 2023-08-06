from .http import Http

class User(object):

    def __init__(self, data: dict, http: Http=None):
        self.raw = data

        self.http = http

        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")
        self.username = data.get("username")
        self.language_code = data.get("language_code")
        self.is_bot = data.get("is_bot")
        self.id = data.get("id")

    async def send(self, text):
        return await self.http.post("sendMessage", {
            "chat_id": self.id,
            "text": text
        })