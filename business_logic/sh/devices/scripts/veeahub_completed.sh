#!/bin/bash

SERIAL_NUMBER=$1

BASEDIR=$(dirname "$0")
executeScriptDownloading="${BASEDIR}/submit_download_log.sh"
executeScriptCompleteConfiguration="${BASEDIR}/submit_configure_log.sh"

sh ${executeScriptDownloading} "/tmp/$SERIAL_NUMBER/device_self_signed_cert.pem" "/tmp/$SERIAL_NUMBER/device_priv.pem" "$SERIAL_NUMBER"
sh ${executeScriptCompleteConfiguration} "/tmp/$SERIAL_NUMBER/device_self_signed_cert.pem" "/tmp/$SERIAL_NUMBER/device_priv.pem" "$SERIAL_NUMBER" "success"