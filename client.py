import os
import time
import socketio
import asyncio


import urllib3
import sys

urllib3.disable_warnings()  # Testing

SERVER_IP = os.environ.get("SERVER_IP", "localhost")


class Client:
    def __init__(self):
        verbose = True
        self.client = socketio.AsyncClient(
            ssl_verify=False,
            logger=verbose,
            engineio_logger=verbose,
            reconnection=False,
        )
        self.received_status = None
        self.client.on("connect", self.on_connected)
        self.client.on("disconnect", self.on_disconnected)
        self.client.on("status", self.on_status_received)

    async def __aenter__(self):
        try:
            await self.client.connect("https://{}:5000".format(SERVER_IP))
        except socketio.exceptions.ConnectionError:
            print("Connection error")
        return self

    async def __aexit__(self, exception_type, exception_value, traceback):
        if self.client.connected:
            await self.client.disconnect()
            await self.client.wait()

    async def on_connected(self):
        print("connection established")
        await self.client.emit(event="subscribe_status", data={"code": "ok"})

    def on_disconnected(self):
        print("disconnected from server")

    def on_status_received(self, data):
        print("data ", data)
        self.received_status = data.get("status", None)

    async def wait_for_status_ok(self):
        while self.client.connected and self.received_status != "ok":
            await self.client.sleep(0.1)


async def wait_for_status_ok():
    async with Client() as sio:
        await sio.wait_for_status_ok()
    return True


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(wait_for_status_ok())
    print("Done")
