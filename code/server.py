import os

import grpc
from keyvaluestore_pb2 import Item, Key, Value, MaybeValue
from keyvaluestore_pb2_grpc import KeyValueStoreServicer as _KeyValueStoreServicer, add_KeyValueStoreServicer_to_server

from utils.grpc_utils import add_servicer_to_server, serve, get_ssl_credentials
from resource import KeyValueStorage


@add_servicer_to_server(add_KeyValueStoreServicer_to_server)
class KeyValueStoreServicer(_KeyValueStoreServicer):
    def __init__(self, storage_path):
        self.storage = KeyValueStorage(storage_path)

    def Get(self, request, context):
        key = request.k
        some, value = False, str()
        if key in self.storage.keys():
            some, value = True, self.storage.__getitem__(key)
        print('get')
        return MaybeValue(some=some, v=Value(v=value))

    def Put(self, request, context):
        key = request.k.k
        value = request.v.v
        some, _value = False, str()
        if key in self.storage.keys():
            some, _value = True, self.storage.__getitem__(key)
        self.storage.__setitem__(key, value)
        self.storage.store()
        print('put')
        return MaybeValue(some=some, v=Value(v=_value))


    def Del(self, request, context):
        key = request.k
        some, value = False, str()
        if key in self.storage.keys():
            some, value = True, self.storage.__getitem__(key)
        self.storage.__delitem__(key)
        self.storage.store()
        print('delete')
        return MaybeValue(some=some, v=Value(v=value))


if __name__ == '__main__':
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    creds = get_ssl_credentials()

    assert host == '[::]'
    assert port == '50051'
    assert creds is not None

    serve(KeyValueStoreServicer('storage.txt'), port, creds)
