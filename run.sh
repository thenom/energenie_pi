#!/bin/bash

source run_config

# setup days of the week
$PYTHON "${CWD}manage.py" loaddata AstralCities.json

$PYTHON "${CWD}manage.py" runserver ${BINDADDR}:${PORT} &
SERVERPID=$!
echo "Started Server [${SERVERPID}]"
$PYTHON "${CWD}sched_run.py" ${CHECKINTER} ${BINDADDR} &
CHECKPID=$!
echo "Started scheduler [${CHECKPID}]"

trap ctrl_c INT

function ctrl_c() {
    kill ${SERVERPID}
    kill ${CHECKPID}
    kill $(ps aux | grep 'manage.py runserver' | grep -v grep | awk '{print $2}')
    exit 0
}

while true; do
    kill -s 0 ${SERVERPID}
    if [ $? -ne 0 ]; then
        echo "Server has died..."
	kill ${CHECKPID}
        exit 1
    fi
    kill -s 0 ${CHECKPID}
    if [ $? -ne 0 ]; then
        echo "Scheduled check has died..."
	kill ${SERVERPID}
        exit 1
    fi
    sleep 1
done
