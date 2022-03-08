# import requests

# r.post(
#     "https://api.bitfinex.com/v2/auth/w/deposit/invoice",
#     data=dict(currency="LNX", wallet="exchange", amount="0.01"),
# )


import os
import sys
from bfxapi import Client, Order
import asyncio

bfx = Client(
    API_KEY="SQEFoRlOrL91GUg8lIh5dFAPjQAJ37vPVDJwqpxDbXe",
    API_SECRET="Tjsp3joFt3VYvD0BqpF8xPgjOWTQk1mZdWjTZA9XwlY",
)


async def run():
    inv = await bfx.rest.generate_invoice("0.009", wallet="exchange", currency="LNX")
    print(inv)


t = asyncio.ensure_future(run())
asyncio.get_event_loop().run_until_complete(t)
