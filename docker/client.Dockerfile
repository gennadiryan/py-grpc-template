FROM python:3.9-slim-bullseye

RUN mkdir /code/
WORKDIR /code/

RUN mkdir protos/ utils/
COPY protos/*.proto protos/
COPY utils/* utils/

RUN mkdir certs/ private/
COPY certs/ca.pem certs/

COPY requirements.txt .
COPY *.py .

RUN pip install -r requirements.txt
RUN ["sh", "utils/gen_code.sh", "protos/keyvaluestore.proto"]
RUN --mount=type=secret,id=ca.key ["sh", "utils/gen_certs.sh", "certs/ca.pem", "/run/secrets/ca.key", "certs/client.pem", "private/client.key", "certs/client.csr", "/CN=client"]

ENTRYPOINT ["/bin/bash"]
