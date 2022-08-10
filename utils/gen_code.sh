#!/bin/bash

gen_code () {
  python -m grpc_tools.protoc --proto_path="$(cd "$(dirname "${1}")" && pwd)" --python_out="$(pwd)" --grpc_python_out="$(pwd)" "$(basename ${1})";
}


gen_code ${1}
