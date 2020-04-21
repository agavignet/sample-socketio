import eventlet
import socketio

import sys
import time


STATUS_SEQUENCE = [
    "asked_starting",
    "starting",
    "started",
    "asked_booting",
    "booting",
    "booted",
    "ask_connecting",
    "connecting",
    "connected",
    "ok",
]


class Server:
    def __init__(self):
        verbose = True
        self.server = socketio.Server(
            logger=verbose, engineio_logger=verbose, cors_allowed_origins=[]
        )
        self.server.on("connect", self.on_connected)
        self.server.on("disconnect", self.on_disconnected)
        self.server.on("subscribe_status", self.on_subscribe_status_received)
        self.clients = []
        self.runner = self.server.start_background_task(self._update_status)

    def _update_status(self):
        while True:
            for status in STATUS_SEQUENCE:
                if self.clients:
                    self.server.emit("status", {"status": status})
                self.server.sleep(0.1)

    def on_connected(self, sid, environ):
        print("connect ", sid)

    def on_disconnected(self, sid):
        print("disconnect ", sid)
        self.clients.remove(sid)

    def on_subscribe_status_received(self, sid, data):
        print("message ", data)
        self.clients.append(sid)


if __name__ == "__main__":
    sio = Server()
    app = socketio.WSGIApp(sio.server)

    # https://eventlet.net/doc/ssl.html
    eventlet.wsgi.server(
        eventlet.wrap_ssl(
            eventlet.listen(("", 5000)), keyfile="server.key", certfile="server.cert"
        ),
        app,
    )
