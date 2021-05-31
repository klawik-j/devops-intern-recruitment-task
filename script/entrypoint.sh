#!/bin/bash
# entrypoint to make sure that both databases are up

echo "Waiting for mysql"
./wait-for-it.sh -t $TIMEOUT $TEST_DB_HOST:$TEST_DB_PORT || exit 1
./wait-for-it.sh -t $TIMEOUT $TARGET_DB_HOST:$TARGET_DB_PORT || exit 1

echo ''
echo '--------------------------'
echo 'Run command'
echo $@
echo '--------------------------'
echo ''
$@ || exit 1