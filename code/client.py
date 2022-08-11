import os

import grpc
from keyvaluestore_pb2 import Item, Key, Value, MaybeValue
from keyvaluestore_pb2_grpc import KeyValueStoreStub

from utils.grpc_utils import get_channel, get_ssl_credentials


class Client:
    def __init__(self, channel):
        self.stub = KeyValueStoreStub(channel)

    def get(self, key):
        response = self.stub.Get(Key(k=key))
        if response.some:
            return response.v.v
        return None

    def put(self, key, value):
        response = self.stub.Put(Item(k=Key(k=key), v=Value(v=value)))
        if response.some:
            return response.v.v
        return None

    def delete(self, key):
        response = self.stub.Del(Key(k=key))
        if response.some:
            return response.v.v
        return None


if __name__ == '__main__':
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    creds = get_ssl_credentials()

    assert host != '[::]'
    assert port == '50051'
    assert creds is not None

    with get_channel(host, port, creds) as channel:
        client = Client(channel)
        print(client.get('a'))
        print(client.put('x', '65'))
        print(client.delete('x'))
        print(client.put('b', 'bye_there'))
        print(client.put('x', 'abc123'))
        print(client.get('x'))