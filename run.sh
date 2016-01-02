#!/bin/bash

CWD="/home/thenom.local/simon.thorley/SimonNas/Energinie RPi/energenie_pi/"
PYTHON=/usr/bin/python
BINDADDR=0.0.0.0
PORT=8000

$PYTHON "${CWD}manage.py" celerybeat &
BEATPID=$!
echo "Started Celerybeat [${BEATPID}]"
$PYTHON "${CWD}manage.py" celeryd &
CELERYPID=$!
echo "Started CeleryD [${CELERYPID}]"
$PYTHON "${CWD}manage.py" runserver ${BINDADDR}:${PORT} &
SERVERPID=$!
echo "Started Server [${SERVERPID}]"

while true; do
    kill -s 0 ${BEATPID}
    if [ $? -ne 0 ]; then
        echo "Celerybeat has died..."
        kill ${CELERYPID}
        kill ${SERVERPID}
        exit 1
    fi
    kill -s 0 ${CELERYPID}
    if [ $? -ne 0 ]; then
        echo "CeleryD has died..."
        kill ${BEATPID}
        kill ${SERVERPID}
        exit 1
    fi
    kill -s 0 ${SERVERPID}
    if [ $? -ne 0 ]; then
        echo "Server has died..."
        kill ${CELERYPID}
        kill ${BEATPID}
        exit 1
    fi
    sleep 1
done
