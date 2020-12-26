#!/bin/bash
if [ $# -lt 3 ]; then
   echo "Usage:"
   echo "  $0 <signer_cert> <signer_priv> <serial_number>"
   echo ""
   echo "<signer_cert> is the certificate of the signer"
   echo "<signer_priv> is the private key used to sign the request"
   echo "<serial_number> is the serial number of the device"
   echo "Example:"
   echo "./scripts/submit_download_log.sh ./keys/device_cert.pem ./keys/device_priv.pem 50-99627-036047"
   exit 255
fi

SIGN_CERT=$1
SIGN_PRIV=$2

ID=$3
LOG=[{\"timestamp\":\"1543870871\",\"action\":\"CONTAINER-BOOTSTRAP\",\"message\":\"Starting\"}]
source ./scripts/submit_log_events.sh $SIGN_CERT $SIGN_PRIV $ID $LOG
