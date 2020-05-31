from websocket_server import WebsocketServer as _WebsocketServer
from .exceptions import NoMessagesError, NoClientEventsError
from .objects import Client, Message, ClientEvent, ClientConnect, ClientDisconnect
from threading import Thread, Lock


class WebSocketServer:
    _message_queue = []
    _client_event_queue = []
    _lock = Lock()
    clients = {}

    def __init__(self, port, host='localhost'):
        self._server = _WebsocketServer(port, host)

        def onmessage(client, server, message):
            with self._lock:
                self._message_queue.append(Message(self.clients[client['id']], message))
        self._server.set_fn_message_received(onmessage)

        def onconnect(client, server):
            with self._lock:
                client = Client(client)
                self.clients[client.id] = client
                self._client_event_queue.append(ClientConnect(client))
        self._server.set_fn_new_client(onconnect)

        def ondisconnect(client, server):
            with self._lock:
                del self.clients[client['id']]
                self._client_event_queue.append(ClientDisconnect(client))
        self._server.set_fn_client_left(ondisconnect)

        self._thread = Thread(target=self._server.run_forever, daemon=True)
        self._thread.start()

    def send(self, message, client=None):
        if client is None:
            if type(message) is list:
                for item in message:
                    Thread(target=self._server.send_message_to_all, args=(item,)).start()
            else:
                self._server.send_message_to_all(message)
        else:
            if type(message) is list:
                for item in message:
                    self._server.send_message(client.dict, item)
            else:
                self._server.send_message(client.dict, message)
    
    @property
    def messages_available(self):
        with self._lock:
            return len(self._message_queue)

    @property
    def first_message(self):
        with self._lock:
            try:
                return self._message_queue.pop(0)
            except IndexError:
                raise NoMessagesError
    
    @property
    def messages(self):
        with self._lock:
            messages = self._message_queue
            if messages:
                self._message_queue = []
                return messages
            else:
                raise NoMessagesError
    
    @property
    def client_events_available(self):
        with self._lock:
            return len(self._client_event_queue)

    @property
    def first_client_event(self):
        with self._lock:
            try:
                return self._client_event_queue.pop(0)
            except IndexError:
                raise NoClientEventsError
    
    @property
    def client_events(self):
        with self._lock:
            client_events = self._client_event_queue
            if client_events:
                self._client_event_queue = []
                return client_events
            else:
                raise NoClientEventsError
