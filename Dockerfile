FROM python:3.9-slim-bullseye

ARG PROTO_NAME
ARG CA_NAME
ARG COMMON_NAME
ARG HOST
ARG PORT
ARG AUTH
ARG CLIENT_AUTH

ENV PROTO_NAME ${PROTO_NAME:-"keyvaluestore"}
ENV CA_NAME ${CA_NAME:-"ca"}
ENV COMMON_NAME ${COMMON_NAME:-"localhost"}
ENV HOST ${HOST:-"[::]"}
ENV PORT ${PORT:-"50051"}
ENV AUTH ${AUTH}
ENV CLIENT_AUTH ${CLIENT_AUTH}

RUN mkdir /app/
WORKDIR /app/

RUN mkdir protos/
COPY protos/${PROTO_NAME}.proto protos/

RUN mkdir code/ code/utils/
COPY code/utils/grpc_utils.py code/utils/
COPY code/utils/gen_code.sh code/utils/
COPY code/utils/gen_cert.sh code/utils/

RUN mkdir certs/ private/
COPY certs/${CA_NAME}.pem certs/
RUN --mount=type=secret,id=key if [ ${AUTH} ] && ( [ ${HOST} = "[::]" ] || [ ${CLIENT_AUTH} ] ); then sh code/utils/gen_cert.sh certs/${CA_NAME}.pem /run/secrets/key certs/${COMMON_NAME}.pem private/${COMMON_NAME}.key certs/${COMMON_NAME}.csr /CN=${COMMON_NAME}; fi;

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY code/*.py code/
RUN sh code/utils/gen_code.sh protos/${PROTO_NAME}.proto code/

EXPOSE ${PORT}
ENTRYPOINT ["/bin/bash"]
