#!/bin/bash
# entrypoint to make sure that database is up

if [$SCRIPT_STATUS -eq 1 -a $RUN_TEST_AFTER_SCRIPT -eq 1] || [$RUN_TEST_MANUAL -eq 1]; then
    echo "Waiting for mysql"
    ./wait-for-it.sh -t $TIMEOUT $TARGET_DB_HOST:$TARGET_DB_PORT || exit 1

    echo ''
    echo '--------------------------'
    echo 'Run command'
    echo $@
    echo '--------------------------'
    echo ''
    $@ || exit 1
else
    sleep 5s
    exit 0
fi