import asyncio

from .message import Message
from .context import Context

class Command(object):

    def __init__(self, executor, name, description, hide):
        self.executor = executor
        self.name = name
        self.description = description
        self.hidden = hide

    def text_to_args(self, text):
        return text.split()[1:]

    def execute(self, message: Message):
        asyncio.create_task(
            self.executor(
                Context(message),
                self.text_to_args(message.text)
            )
        )

    def to_botcommand(self):
        return {
            "command": self.name,
            "description": self.description
        }