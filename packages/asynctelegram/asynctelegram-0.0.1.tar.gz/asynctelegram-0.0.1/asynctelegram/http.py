from aiohttp import ClientSession
from urllib import parse

from json import dumps
from typing import Union

class Http(object):

    def __init__(self, token: str, base_url: str="https://api.telegram.org/bot", session_params: dict=None):

        if session_params is None:
            session_params = {}

        session_params["read_timeout"] = 0

        self.session = ClientSession(**session_params)
        self.base_url = base_url
        self.token = token

    async def close(self):
        await self.session.close()

    def get_url(self, method: str, data: dict={}):
        return self.base_url+self.token+"/"+method+"?"+parse.urlencode(data)

    async def get(self, method: str, data: dict={}) -> Union[dict, list]:
        async with self.session.get(self.get_url(method, data=data)) as resp:
            resp.raise_for_status()
            tmp = await resp.json()
            if not tmp["ok"]:
                raise Exception()
            return tmp["result"]

    async def post(self, method: str, data: dict={}) -> Union[dict, list]:
        async with self.session.post(self.get_url(method), data=dumps(data), headers={"Content-Type": "application/json"}) as resp:
            resp.raise_for_status()
            tmp = await resp.json()
            if not tmp["ok"]:
                raise Exception()
            return tmp["result"]