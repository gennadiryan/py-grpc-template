# Python GRPC Template

## Usage Modes
This Python GRPC Template is designed to mitigate the boilerplate involved in setting up a GRPC server/client pair in Python, and further, in containerizing such a network. The module features some utilities to automate the most common semantics of server and client stub instantiation. The server and client code thus can be written independently of the backend connection and authentication mechanisms. These auth mechanisms include generation of build-time leaf certificates from root certificates, as well as self-signed root certificates for testing (and deployment, although this is not recommended for public-facing productions).

The primary goal of this project is to allow for server and client (Docker) container nodes to be generated with minimal overhead. Ideally, this template would exist simply as an image layer which complements an already-containerized service. In this direction, the number of distinct Dockerfiles shall be reduced from two to one, as the differences between the two builds are minimal, and vanish when considering that many presently hardcoded values will be parameterized in the future. Thus this project will soon allow building a server or client instance from the same underlying template image layer, with the two differentiated only by their build parameters, and any additional image layers needed for the implementation.

At present, the implementation has been tested both on bare metal, and in Docker containers sharing a bridge network. A bridge network creates a local DNS and allows for the container names to be used in referencing one another. A docker compose implementation will be added to automate the creation and management of the network and the plugging of parameters to server and client instances. This allows for replication of nodes with potentially different image layers above the template layer, and allows for nodes across different machines (i.e. on an overlay network) to be associated in a single configuration. Additionally, such an implementation can be endowed with a set of Kubernetes Deployments and Services, and run with Docker Desktop's native Kubernetes cluster. Note that when this project has met its goals, it will be possible to specify arbitrary containers as GRPC nodes entirely by configuring the docker compose file.

## Security

The utils/gen_certs.sh file implements bash commands to

1. create a self-signed root certificate (to serve as a certificate authority), and
1. create new leaf certificates from a given root certificate.

Their specifications are as follows:

1. `gen_root_cert [path_to_cert] [path_to_pkey] [subject]`, and
1. `gen_signed_cert [path_to_ca_cert] [path_to_ca_key] [path_to_cert] [path_to_pkey] [path_to_cert_sign_request] [subject]`,

where `[subject]` denotes the subject field which is required in new certificates and certificate requests. When creating a root cert, minimally use `/O=[owner]`. When creating a leaf from this certificate, it will feature `[owner]` as the certificate issuer. When creating a leaf, be sure to minimally specify `/CN=[common_name]`. When containerized, this value must match the server's DNS name to validate the connection. Docker uses the container's name as its DNS name on user-defined bridge and overlay networks.

## References
This project was inspired in part by Dan Hipschman's [Python Microservices GRPC tutorial](https://realpython.com/python-microservices-grpc/). The reader is also referred to the official [Python GRPC API Reference](https://grpc.github.io/grpc/python/) for further documentation, and GRPC's [python examples](https://github.com/grpc/grpc/tree/master/examples/python). The examples outline many common use cases; some relevant ones include:
- helloworld
- hellostreamingworld
- auth
- route_guide
