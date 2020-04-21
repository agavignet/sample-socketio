# sample-socketio

This repo is related to https://github.com/miguelgrinberg/python-socketio/issues/451
and aims to reproduce the issue easily.

## Setup

One machine should run the server.
One machine should run the client.

Both machines are on the same local network.

* Create a clean Python3 virtualenv (I'm personaly having `Python 3.7.3`)
* Install deps: `pip3 install -r requirements.txt`

## Server side

### Description

When at least one client is connected, the server sends status update through SocketIO (default namespace).

### Run

`python3 server.py`

## Client side

### Description

Client connects to the server and subscribes for the status update event. Then it waits until the status received is OK.

### Run

`export SERVER_IP=<local_server_ip>`

#### Check

`python3 client.py`

#### Stress test (run n clients)

`python3 nclient.py --count 10`

## Results

After running the stress test few times (I reproduce the problem every ~8 runs), you should see one of the following errors:

```
$ python3 nclient.py --count 10
...
Unexpected error "[Errno 9] Bad file descriptor", aborting
...
```

```
$ python3 nclient.py --count 10
Starting 10 client
...
Exception in thread Thread-3:
Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 917, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.7/threading.py", line 865, in run
    self._target(*self._args, **self._kwargs)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/engineio/client.py", line 683, in _write_loop
    self.ws.send(encoded_packet)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_core.py", line 253, in send
    return self.send_frame(frame)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_core.py", line 279, in send_frame
    l = self._send(data)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_core.py", line 449, in _send
    return send(self.sock, data)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_socket.py", line 157, in send
    return _send()
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_socket.py", line 139, in _send
    return sock.send(data)
  File "/usr/lib/python3.7/ssl.py", line 986, in send
    return super().send(data, flags)
OSError: [Errno 9] Bad file descriptor
...
```

```
Exception in thread Thread-3:
Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 917, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.7/threading.py", line 865, in run
    self._target(*self._args, **self._kwargs)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/engineio/client.py", line 683, in _write_loop
    self.ws.send(encoded_packet)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_core.py", line 253, in send
    return self.send_frame(frame)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_core.py", line 279, in send_frame
    l = self._send(data)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_core.py", line 449, in _send
    return send(self.sock, data)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_socket.py", line 157, in send
    return _send()
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_socket.py", line 139, in _send
    return sock.send(data)
  File "/usr/lib/python3.7/ssl.py", line 984, in send
    return self._sslobj.write(data)
ssl.SSLError: [SSL: BAD_LENGTH] bad length (_ssl.c:2341)
```

```
Exception in thread Thread-3:
Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 917, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.7/threading.py", line 865, in run
    self._target(*self._args, **self._kwargs)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/engineio/client.py", line 683, in _write_loop
    self.ws.send(encoded_packet)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_core.py", line 253, in send
    return self.send_frame(frame)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_core.py", line 279, in send_frame
    l = self._send(data)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_core.py", line 449, in _send
    return send(self.sock, data)
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_socket.py", line 157, in send
    return _send()
  File "/home/adrien/.virtualenvs/sio/lib/python3.7/site-packages/websocket/_socket.py", line 139, in _send
    return sock.send(data)
  File "/usr/lib/python3.7/ssl.py", line 984, in send
    return self._sslobj.write(data)
ssl.SSLEOFError: EOF occurred in violation of protocol (_ssl.c:2341)
```

## Notes

With a real app, those errors are visible on various CI environment (Bitrise, CircleCI for example).

Setting `enable_multithread=True` here https://github.com/miguelgrinberg/python-engineio/blob/master/engineio/client.py#L377 solves the problem.
