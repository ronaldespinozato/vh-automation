#!/bin/bash
if [ $# -lt 4 ]; then
   echo "Usage:"
   echo "  $0 <signer_cert> <signer_priv> <serial_number> <logs>"
   echo ""
   echo "<signer_cert> is the certificate of the signer"
   echo "<signer_priv> is the private key used to sign the request"
   echo "<serial_number> is the serial number of the device"
   echo "<logs> is an array of objects with timestamp, action, message and extra field"
   echo "Example:"
   echo "./scripts/submit_log_events.sh ./keys/device_cert.pem ./keys/device_priv.pem 50-99627-036047 [{\"timestamp\":\"1543870871\",\"action\":\"save\",\"message\":\"logging save action\",\"extra\":{\"sub_extra\":\"\"}},{\"timestamp\":\"1543870871\",\"action\":\"update\",\"message\":\"logging update action\"}]"
   exit 255
fi

SIGN_CERT=$1
SIGN_PRIV=$2

ID=$3
LOGS=$4

REQ_URL="/devices/${ID}/logs"
REQ_METHOD=POST
export LOGS
envsubst < scripts/logs.tmpl | scripts/send_request.sh ${SIGN_CERT} ${SIGN_PRIV} ${REQ_URL} ${REQ_METHOD}

