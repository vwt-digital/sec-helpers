#!/bin/bash

exit_code=0

printf "\nRunning SSL3 test\n"
ssl3=$(bash ssl3.sh "$1")
# shellcheck disable=SC2181
[ $? -eq 0 ] || exit_code=1

printf "\nRunning TLS test\n"
protocol=$(python main.py "$1")
# shellcheck disable=SC2181
[ $? -eq 0 ] || exit_code=1

printf "\nSSL3 test output:\n"
echo "$ssl3"

printf "\nTLS test output:\n"
echo "$protocol"
exit $exit_code
