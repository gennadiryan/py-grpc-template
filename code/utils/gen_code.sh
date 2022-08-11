#!/bin/bash

gen_code () {
  python -m grpc_tools.protoc --proto_path="$(cd "$(dirname "${1}")" && pwd)" --python_out="${2}" --grpc_python_out="${3}" "$(basename ${1})";
}


if [ $# -gt 0 ];
then
  if [ $# -eq 1 ];
  then
    gen_code ${1} $(pwd);
  elif [ $# -eq 2 ];
  then
    gen_code ${1} ${2} ${2};
  else
    gen_code ${1} ${2} ${3};
  fi;
fi;
