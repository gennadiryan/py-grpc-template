#!/bin/bash

gen_root_cert () {
  openssl req -x509 -new -newkey rsa:2048 -nodes -out ${1} -keyout ${2} -set_serial 0 -subj ${3};
}

gen_signed_cert () {
  openssl req -new -newkey rsa:2048 -nodes -out ${5} -keyout ${4} -subj ${6};
  openssl x509 -req -CA ${1} -CAkey ${2} -in ${5} -out ${3} -set_serial 0;
}


gen_signed_cert ${1} ${2} ${3} ${4} ${5} ${6}
