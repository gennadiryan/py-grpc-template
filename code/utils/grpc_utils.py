import os
from functools import wraps

from concurrent import futures
import grpc


# Use func.__name__ to preserve the function name
def add_method(func):
    def wrap(cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return cls
    return wrap


# Omit `add_to_server=wraps(func)(add_to_server)` to use
#   the name 'add_to_server' instead of
#   the name func.__name__ == f'add_{service}Servicer_to_server'
def add_servicer_to_server(func):
    def add_to_server(self, server):
        return func(self, server)
    return add_method(add_to_server)


def serve(servicer, port, credentials=None):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer.add_to_server(server)

    if credentials is None:
        server.add_insecure_port(f'[::]:{port}')
    else:
        server.add_secure_port(f'[::]:{port}', credentials)

    server.start()
    server.wait_for_termination()


def get_channel(host, port, credentials=None):
    if credentials is None:
        return grpc.insecure_channel(f'{host}:{port}')
    return grpc.secure_channel(f'{host}:{port}', credentials)


def ssl_credentials(root_certs=None, key_cert_pairs=None, server=False, client_auth=False):
    def get_root_certs(root_certs):
        with open(root_certs, 'rb') as f:
            return f.read()

    def get_key_cert_pairs(key_cert_pairs):
        pairs = list()
        for key, cert in key_cert_pairs:
            pair = list()
            with open(key, 'rb') as f:
                pair.append(f.read())
            with open(cert, 'rb') as f:
                pair.append(f.read())
            pairs.append(tuple(pair))
        return pairs

    if server:
        assert key_cert_pairs is not None
        key_cert_pairs = get_key_cert_pairs(key_cert_pairs)
        if client_auth:
            assert root_certs is not None
            root_certs = get_root_certs(root_certs)
        else:
            root_certs = None
        return grpc.ssl_server_credentials(
            key_cert_pairs,
            root_certificates=root_certs,
            require_client_auth=client_auth,
        )

    assert root_certs is not None
    root_certs = get_root_certs(root_certs)
    if client_auth:
        assert key_cert_pairs is not None
        assert len(key_cert_pairs) == 1
        key_cert_pairs = get_key_cert_pairs(key_cert_pairs)
    else:
        key_cert_pairs = [(None,) * 2]
    return grpc.ssl_channel_credentials(
        root_certificates=root_certs,
        private_key=key_cert_pairs[0][0],
        certificate_chain=key_cert_pairs[0][1],
    )


def get_ssl_credentials():
    is_host = os.getenv('HOST_NAME') == '[::]'

    common = os.getenv('COMMON_NAME')
    ca = os.getenv('CA_NAME')
    auth = os.getenv('AUTH') == 'true'
    client_auth = os.getenv('CLIENT_AUTH') == 'true'

    credentials = None
    if auth:
        root_certs = f'/app/certs/{ca}.pem' if (is_host and client_auth) or ((not is_host) and auth) else None
        key_cert_pairs = [(f'/app/private/{common}.key', f'/app/certs/{common}.pem')] if (is_host and auth) or ((not is_host) and client_auth) else None
        credentials = ssl_credentials(
            root_certs=root_certs,
            key_cert_pairs=key_cert_pairs,
            server=is_host,
            client_auth=client_auth,
        )

    return credentials
