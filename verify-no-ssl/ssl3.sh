#!/bin/bash

ssl=$(timeout 5 /usr/local/bin/openssl s_client -connect "$1":443 -ssl3)
echo $?
echo "$ssl"
if [[ $ssl == *"Verify return code: 0 (ok)"* ]]; then
  echo "No sign of SSLv3 allowance found"
  exit 0
fi
if [[ $ssl == *"END CERTIFICATE"* ]]; then
  echo "SSLv3 is allowed"
  exit 1
fi
echo "Failed to check SSLv3"
exit 1
