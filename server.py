import grpc
from keyvaluestore_pb2 import Item, Key, Value, MaybeValue
from keyvaluestore_pb2_grpc import KeyValueStoreServicer as _KeyValueStoreServicer, add_KeyValueStoreServicer_to_server

from utils.grpc_utils import add_servicer_to_server, serve, ssl_credentials
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
    # creds = None # insecure
    #
    # creds = ssl_credentials(
    #     key_cert_pairs=[('private/server.key', 'certs/server.pem')],
    #     server=True,
    #     client_auth=False,
    # ) # one-way secure

    creds = ssl_credentials(
        root_certs='certs/ca.pem',
        key_cert_pairs=[('private/server.key', 'certs/server.pem')],
        server=True,
        client_auth=True,
    ) # two-way secure

    serve(KeyValueStoreServicer('storage.txt'), 50051, creds)
