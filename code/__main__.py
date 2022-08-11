if __name__ == '__main__':
    host = os.getenv('HOST_NAME')
    common = os.getenv('COMMON_NAME')
    port = os.getenv('PORT')
    ca = os.getenv('CA_NAME')
    use_ca = int(os.getenv('USE_CA')) > 0
    use_key = int(os.getenv('USE_KEY')) > 0



    host = os.getenv('HOST_NAME')
    client = os.getenv('COMMON_NAME')
    port = os.getenv('PORT')
    ca = os.getenv('CA_NAME')
    auth = int(os.getenv('USE_CA')) > 0
    client_auth = int(os.getenv('USE_KEY')) > 0

    creds = None
    if auth:
        creds = ssl_credentials(
            root_certs=f'certs/{CA_NAME}.pem',
            key_cert_pairs=[(f'private/{client}.key', f'certs/{client}.pem')] if client_auth else None,
            server=False,
            client_auth=client_auth,
        )

    with get_channel(host, port, creds) as channel:
        client = Client(channel)
        print(client.get('a'))
        print(client.put('x', '65'))
        print(client.delete('x'))
        print(client.put('b', 'bye_there'))
        print(client.put('x', 'abc123'))
        print(client.get('x'))

if __name__ == '__main__':
    host = os.getenv('COMMON_NAME')
    port = os.getenv('PORT')
    ca = os.getenv('CA_NAME')
    auth = int(os.getenv('USE_KEY')) > 0
    client_auth = int(os.getenv('USE_CA')) > 0

    creds = None
    if auth:
        creds = ssl_credentials(
            root_certs=f'certs/{ca}.pem' if client_auth else None,
            key_cert_pairs=[(f'private/{host}.key', f'certs/{host}.pem')],
            server=True,
            client_auth=client_auth,
        )

    serve(KeyValueStoreServicer('storage.txt'), port, creds)
