import os
import time
import socketio

import urllib3
import sys

urllib3.disable_warnings()  # Testing

SERVER_IP = os.environ.get("SERVER_IP", "localhost")


class Client:
    def __init__(self):
        verbose = True
        self.client = socketio.Client(
            ssl_verify=False,
            logger=verbose,
            engineio_logger=verbose,
            reconnection=False,
        )
        self.received_status = None
        self.client.on("connect", self.on_connected)
        self.client.on("disconnect", self.on_disconnected)
        self.client.on("status", self.on_status_received)

    def __enter__(self):
        try:
            self.client.connect("https://{}:5000".format(SERVER_IP))
        except socketio.exceptions.ConnectionError:
            print("Connection error")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.client.connected:
            self.client.disconnect()

    def on_connected(self):
        print("connection established")
        self.client.emit(event="subscribe_status", data={"code": "ok"})

    def on_disconnected(self):
        print("disconnected from server")

    def on_status_received(self, data):
        print("data ", data)
        self.received_status = data.get("status", None)

    def wait_for_status_ok(self):
        while self.client.connected and self.received_status != "ok":
            time.sleep(0.1)


if __name__ == "__main__":
    with Client() as sio:
        sio.wait_for_status_ok()
    sio.client.wait()
    print("Done")
