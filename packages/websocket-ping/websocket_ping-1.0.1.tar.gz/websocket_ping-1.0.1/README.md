## ping_ws.py usage

### setup
#### To install pip package
```
pip install websocket-ping
```

#### For dev version
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements_ws_ping.txt
```


### cli interface
-w flag is for the websocket endpoint
-d is the duration to test if the connection is maintained (in seconds)
```
python -m ping_ws.ping_ws -w wss://host/ws/ping/ -d [int]
```

### examples
```
# Failure to connect - server rejecting connection
(.venv) $ python -m ping_ws.ping_ws -w wss://host/ws/ping/
Connection to wss unsuccessful: server rejected WebSocket connection: HTTP 502


# Success on connection
(.venv) $ python -m ping_ws.ping_ws -w ws://localhost:8000/ws/ping/
Successfully connected to ws://localhost:8000/ws/ping/, response to ping: pong
Maintained connection to ws://localhost:8000/ws/ping/, response to ping: pong
Success!


```

