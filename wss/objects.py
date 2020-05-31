class Client:
    def __init__(self, cdict):
        self.id = cdict['id']
        self.address = cdict['address'][0]
        self.port = cdict['address'][1]
        self.dict = cdict


class Message:
    def __init__(self, client, message):
        self.client = client
        self.data = message


class ClientEvent:
    def __init__(self, client):
        self.client = client


class ClientConnect(ClientEvent):
    pass


class ClientDisconnect(ClientEvent):
    pass
