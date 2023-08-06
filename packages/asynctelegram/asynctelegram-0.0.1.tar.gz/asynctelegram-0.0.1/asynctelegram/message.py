from .http import Http
from .user import User
from .chat import Chat

class Message(object):
    
    def __init__(self, data: dict, http: Http=None):
        self.raw = data

        self.http = http
        self.author = User(data.get("from"), http=http) if data.get("from") else None
        self.chat = Chat(data.get("chat"), http=http)

        self.id = data.get("message_id")
        self.date = data.get("date")
        self.text = data.get("text")
