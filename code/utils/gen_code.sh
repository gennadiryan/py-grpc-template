#!/bin/bash

gen_code () {
  python -m grpc_tools.protoc --proto_path="$(cd "$(dirname "${1}")" && pwd)" --python_out="${2}" --grpc_python_out="${2}" "$(basename ${1})";
}


if [ $# -gt 0 ];
then
  if [ $# -eq 1 ];
  then
    gen_code ${1} $(pwd);
  else
    gen_code ${@};
  fi;
fi;
