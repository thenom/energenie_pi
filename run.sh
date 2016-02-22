#!/bin/bash

CWD="/usr/local/energenie_pi/"
PYTHON=/usr/bin/python
BINDADDR=0.0.0.0
PORT=8000

# setup days of the week
$PYTHON "${CWD}manage.py" loaddata AstralCities.json

$PYTHON "${CWD}manage.py" celerybeat &
BEATPID=$!
echo "Started Celerybeat [${BEATPID}]"
$PYTHON "${CWD}manage.py" celeryd &
CELERYPID=$!
echo "Started CeleryD [${CELERYPID}]"
$PYTHON "${CWD}manage.py" runserver ${BINDADDR}:${PORT} &
SERVERPID=$!
echo "Started Server [${SERVERPID}]"

trap ctrl_c INT

function ctrl_c() {
    kill ${CELERYPID}
    kill ${SERVERPID}
    kill ${BEATPID}
    kill $(ps aux | grep 'manage.py runserver' | grep -v grep | awk '{print $2}')
    exit 0
}

while true; do
    kill -s 0 ${BEATPID}
    if [ $? -ne 0 ]; then
        echo "Celerybeat has died..."
        kill ${CELERYPID}
        kill ${SERVERPID}
        killall $(ps aux | grep 'manage.py runserver' | awk '{print $2}')
        exit 1
    fi
    kill -s 0 ${CELERYPID}
    if [ $? -ne 0 ]; then
        echo "CeleryD has died..."
        kill ${BEATPID}
        kill ${SERVERPID}
        killall $(ps aux | grep 'manage.py runserver' | awk '{print $2}')
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
