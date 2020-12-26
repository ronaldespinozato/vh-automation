#!/bin/bash
if [ $# -lt 4 ]; then
   echo "Usage:"
   echo "  $0 <signer_certificate_file_path> <signer_priv_key_file_path> <url> <method> [request_json]"
   echo ""
   echo "<method> is one of 'GET', 'POST', 'PUT', or 'DELETE'"
   echo "If the [request_json] argument is not specified, then it is read from stdin"
   exit 255
fi

CERT=$1
PRIV=$2

REQ_HOST=${VEEA_BOOTSTRAP_SERVER}
if [ -z "$REQ_HOST" ]
then
	echo "No Bootstrap Server seems to have been set in the environment. Execution must be aborted."
	exit 1
fi
REQ_URL=$3
REQ_METHOD=$4
REQ_TIMESTAMP=$(curl -k -s $VEEA_BOOTSTRAP_SERVER/timestamp | awk -F"[,:}]" '{print $2}')
REQ_BODY=$( sed 's/^/    /g' "${5:-/dev/stdin}" )
export REQ_URL REQ_METHOD REQ_TIMESTAMP REQ_BODY
echo "Using key ${PRIV} and certificate ${CERT} to sign a ${REQ_METHOD} request to ${VEEA_BOOTSTRAP_SERVER}${REQ_URL}"
envsubst < scripts/request.tmpl | openssl cms -sign -inkey ${PRIV} -signer ${CERT} \
  -outform DER -nosmimecap -nodetach -binary -noattr | curl --insecure -X ${REQ_METHOD} --form "request=@-" $VEEA_BOOTSTRAP_SERVER${REQ_URL} -i
