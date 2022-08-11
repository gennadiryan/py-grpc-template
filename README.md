# Python GRPC Template

## Updates
- ### 11/08/22
  - Added interactive `get`, `put`, `delete` implementation to the client container. Revised environment variable representation of configs. Added option flags to `utils/gen_cert.sh` to clarify usage of different build-time auth configurations.
- ### 11/07/022
  - First push

## Usage Modes
This Python GRPC Template is designed to mitigate the boilerplate involved in setting up a GRPC server/client pair in Python, and further, in containerizing such a network. The module features some utilities to automate the most common semantics of server and client stub instantiation. The server and client code thus can be written independently of the backend connection and authentication mechanisms. These auth mechanisms include generation of build-time leaf certificates from root certificates, as well as self-signed root certificates for testing. Deployments, however, should use trusted root certificates, either obtained from a known public Certificate Authority, or generated by an internal organizational Certificate Authority.

The primary aim of this project is to allow for server and client (Docker) container nodes to be generated with minimal overhead. This template functions as an image layer which complements an already-containerized service. In this direction, the number of distinct Dockerfiles has been reduced from two to one, as the differences between the two builds were minimal, and vanished when hardcoded values were parameterized as build arguments and environment variables. Thus this project now allows building a server or client instance from the same underlying template image layer, with the two differentiated only by their build parameters. This means that client and server functionality are treated as a unit, and it is less challenging to debug such issues, as the server and client share the boilerplate configs and code that define the networking and auth functionality.

At present, the implementation has been tested on bare metal, and in Docker containers sharing a bridge network. A bridge network creates a local DNS and allows for container names to be used in referencing one another.

>[NOTE: The build-time parameter COMMON_NAME should correspond to this DNS name, and is used to set the corresponding name field in any certificates that are generated. You may still use the container without providing this setting, but it is necessary if you intend to use authentication with that container].

A docker compose implementation is being developed to automate the creation and management of the network and the plugging of parameters to server and client instances. This allows for replication of nodes with potentially different image layers above and/or below the template layer, and allows for nodes across different machines (i.e. on an overlay network) to be associated in a single configuration. Additionally, such an implementation can be endowed with a set of Kubernetes Deployments and Services, and run with Docker Desktop's native Kubernetes cluster.

## Security

The utils/gen_cert.sh file implements bash commands to

1. create a self-signed root certificate (to serve as a certificate authority), and
1. create new leaf certificates from a given root certificate.

Their specifications are as follows:

1. `gen_root_cert [path_to_cert] [path_to_pkey] [subject]`, and
1. `gen_signed_cert [path_to_ca_cert] [path_to_ca_key] [path_to_cert] [path_to_pkey] [path_to_cert_sign_request] [subject]`,

where `[subject]` denotes the subject field which is required in new certificates and certificate requests. When creating a root cert, minimally use `/O=[owner]`. When creating a leaf from this certificate, it will feature `[owner]` as the certificate issuer. When creating a leaf, be sure to minimally specify `/CN=[common_name]`. When containerized, this value must match the server's DNS name to validate the connection. Docker uses the container's name as its DNS name on user-defined bridge and overlay networks.

The bash script itself, when run with parameters, behaves a bit differently. Its specification is as follows:

```
sh utils/gen_cert.sh -a [AUTH] -c [CLIENT_AUTH] -h [HOST_NAME] [CA_NAME] [COMMON_NAME] [KEY]
```

The options (`-a`, `-c`, `-h`) are all required (in any order), as are their respective parameters (one each) and the three positional parameters that follow them. This script has a very specific purpose (namely, ensuring reproducible and correct implementation of certificate signing during Docker builds), so it does not attempt to handle arguments that deviate from this pattern at this time. The option parameter values must each be one of `"true"` or `"false"`. This is intentional, to catch any instance in which a misconfiguration has led to the script being run with faulty values. The remaining values are fairly self-explanatory. `CA_NAME` is the plaintext name of the certificate authority being used to validate connections in this container. `COMMON_NAME` is the plaintext DNS name used over the network for the container. `KEY` refers to the location of the private key with which to sign the certificate. Note that this key can be securely passed in several ways. Docker provides secret mounts during build time which are only available on the container for the duration of a single instruction. Additionally, the underlying SSL tool (openssl) supports private key encryption via passwords. This can manifest either as a request for password entry from the command line, or as a "passed-in" password via another file. This encryption may be applied both to the ephemeral authority's private key, and the internal container key which is generated alongside its signed certificate. It is recommended for production purposes that both keys be password-protected if the password can be provided securely, but it is not strictly necessary for every threat model, and may indeed present a greater risk than an unencrypted key for some setups.


## References
This project was inspired in part by Dan Hipschman's [Python Microservices GRPC tutorial](https://realpython.com/python-microservices-grpc/). For security matters at a greater depth, refer to Ivan Ristić's [OpenSSL Cookbook](https://www.feistyduck.com/books/openssl-cookbook/). The reader is also referred to the official [OpenSSL Documentation](https://www.openssl.org/docs/) and [Python GRPC API Reference](https://grpc.github.io/grpc/python/) for further information, and GRPC's [python examples](https://github.com/grpc/grpc/tree/master/examples/python). The GRPC examples outline many common use cases; some relevant ones include:
- helloworld
- hellostreamingworld
- auth
- route_guide
