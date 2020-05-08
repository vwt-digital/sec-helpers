#!/bin/bash
cipherscan=$(./cipherscan/cipherscan "$1")
analyzer=$(./cipherscan/analyze.py -t "$1")
echo "$cipherscan"

if echo "$cipherscan" | grep -q "connection failed"; then
  printf "\nSomething went wrong. Check the logs above.\n"
  exit 1
fi
echo "$analyzer"

exit_code=0
printf "\nREPORT:\n\n"
if echo "$cipherscan" | sed -n -e 's/^.*SSL 3.254//p' | grep -q "absent"; then
  echo "SSL 3.254 is allowed."
  exit_code=1
fi
if echo "$cipherscan" | sed -n -e 's/^.*TLS 1.0//p' | grep -q "absent"; then
  echo "TLS 1.0 is allowed."
  exit_code=1
fi
if echo "$cipherscan" | sed -n -e 's/^.*TLS 1.1//p' | grep -q "absent"; then
  echo "TLS 1.1 is allowed."
  exit_code=1
fi
intermediate=$(echo "$analyzer" | sed -n '/intermediate/,/^\s*$/p' | sed '/consider/d')
# shellcheck disable=SC2063
if echo "$intermediate" | grep -q '*'; then
  printf "\nIntermediate requirements not satisfied:\n"
  echo "$intermediate"
  exit_code=1
fi

if [ "$exit_code" -eq "0" ]; then
  echo "Testing was successful"
fi
exit $exit_code
