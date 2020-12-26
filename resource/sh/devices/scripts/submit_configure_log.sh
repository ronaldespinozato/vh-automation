#!/bin/bash
if [ $# -lt 4 ]; then
   echo "Usage:"
   echo "  $0 <signer_cert> <signer_priv> <serial_number> <status>"
   echo ""
   echo "<signer_cert> is the certificate of the signer"
   echo "<signer_priv> is the private key used to sign the request"
   echo "<serial_number> is the serial number of the device"
   echo "<status> is the result of configure and install process could be success/error"
   echo "Example:"
   echo "./scripts/submit_configure_log.sh ./keys/device_cert.pem ./keys/device_priv.pem 50-99627-036047 success"
   exit 255
fi

SIGN_CERT=$1
SIGN_PRIV=$2

ID=$3
STATUS=$4
LOG=[{\"timestamp\":\"1543870871\",\"action\":\"CONTAINER-BOOTSTRAP\",\"message\":\"$STATUS\"}]
source ./scripts/submit_log_events.sh $SIGN_CERT $SIGN_PRIV $ID $LOG
