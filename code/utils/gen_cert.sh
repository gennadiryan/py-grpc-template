#/bin/bash


_KEY_TYPE="rsa:2048"

gen_root_cert () {
  openssl req -x509 -new -newkey ${_KEY_TYPE} -nodes -out ${1} -keyout ${2} -set_serial 0 -subj ${3};
}

gen_signed_cert () {
  openssl req -new -newkey ${_KEY_TYPE} -nodes -out ${5} -keyout ${4} -subj ${6};
  openssl x509 -req -CA ${1} -CAkey ${2} -in ${5} -out ${3} -set_serial 0;
}


parse_bool () {
  if [ "${1}" = "true" ]; then true;
  elif [ "${1}" = "false" ]; then false;
  else echo "Boolean is not one of \"true\" or \"false\""; exit 1;
  fi;
}

parse_args () {
  _AUTH=false;
  _CLIENT_AUTH=false;
  _IS_HOST=false;

  while getopts "a:c:h:" opt; do
    case $opt in
      a) if parse_bool ${OPTARG}; then _AUTH=true; fi;;
      c) if parse_bool ${OPTARG}; then _CLIENT_AUTH=true; fi;;
      h) if [ ${OPTARG} = "[::]" ]; then _IS_HOST=true; fi;;
      :) echo "Option requires argument: -${opt}"; exit 1;;
      ?) echo "Unrecognized option"; exit 1;;
    esac;
  done;

  if ${_AUTH} && ( ${_CLIENT_AUTH} || ${_IS_HOST} ); then true;
  else false;
  fi;
}


if [ $# -gt 0 ]; then
  if parse_args $@; then
    shift $((${OPTIND} - 1));

    _CA_NAME=${1};
    _COMMON_NAME=${2};
    _KEY=${3};

    if ! [ -f ${_KEY} ]; then
      echo "File not found: private key at ${_KEY}"; exit 1;
    fi; if ! ( gen_signed_cert "certs/${_CA_NAME}.pem" "${_KEY}" "certs/${_COMMON_NAME}.pem" "private/${_COMMON_NAME}.key" "certs/${_COMMON_NAME}.csr" "/CN=${_COMMON_NAME}" ); then
      echo "Failed to generate signed certificate"; exit 1;
    fi; echo "Signed certificate generated"; exit 0;
  else
    echo "No signed certificate generated"; exit 0;
  fi;
fi;
