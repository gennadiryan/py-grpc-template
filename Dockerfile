FROM python:3.9-slim-bullseye

ARG PROTO_NAME
ARG CA_NAME
ARG COMMON_NAME
ARG AUTH
ARG CLIENT_AUTH
ARG HOST
ARG PORT

ENV PROTO_NAME ${PROTO_NAME:-"keyvaluestore"}
ENV CA_NAME ${CA_NAME:-"ca"}
ENV COMMON_NAME ${COMMON_NAME:-"localhost"}
ENV AUTH ${AUTH:-"false"}
ENV CLIENT_AUTH ${CLIENT_AUTH:-"false"}
ENV HOST_NAME ${HOST:-"[::]"}
ENV PORT ${PORT:-"50051"}

RUN mkdir /app/
WORKDIR /app/

RUN mkdir protos/
COPY protos/${PROTO_NAME}.proto protos/

RUN mkdir code/ code/utils/
COPY code/utils/gen_cert.sh code/utils/
COPY code/utils/gen_code.sh code/utils/
COPY code/utils/grpc_utils.py code/utils/

RUN mkdir certs/ private/
COPY certs/${CA_NAME}.pem certs/
RUN --mount=type=secret,id=key sh -u code/utils/gen_cert.sh -a "${AUTH}" -c "${CLIENT_AUTH}" -h "${HOST_NAME}" "${CA_NAME}" "${COMMON_NAME}" "/run/secrets/key"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY code/*.py code/
RUN sh code/utils/gen_code.sh protos/${PROTO_NAME}.proto code/

EXPOSE ${PORT}
ENTRYPOINT ["/bin/bash"]
