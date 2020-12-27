#!/bin/bash

if [ $# -lt 1 ]; then
   echo "Usage:"
   echo "  $0 <environment>"
   echo ""
   echo "<environment> is dev/local/qa"
   echo "Example:"
   echo ". ./set_environment.sh qa"
   exit 255
fi

ENV=$1

ENV_CONTEXT=$(case $1 in
  "dev") echo "/bootstrap" ;;
  "local") echo "" ;;
  "qa") echo "" ;;
  *) echo "" ;;
esac)

SERVER=$(case $1 in
  "dev") echo "https://dev.veea.co/bootstrap" ;;
  "local") echo "http://localhost:9020" ;;
  "qa") echo "https://qabootstrap.veea.io" ;;
  *) echo "https://localhost:8080" ;;
esac)

echo $ENV_CONTEXT
echo $SERVER

export BASE_PATH=$ENV_CONTEXT
export VEEA_BOOTSTRAP_SERVER=$SERVER

