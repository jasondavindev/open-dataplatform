#!/bin/bash
TOPIC=$1
DELAY=$2

[ -z "$TOPIC" -o -z "$DELAY" ] && echo "Usage script.sh topic-name delay" && exit 1

USERNAMES=('John' 'Mary' 'Cris')
PAGES=('home' 'users' 'login')
EVENT_NAMES=('click' 'scroll' 'submit')

PAYLOAD='{
    "username": "USERNAME",
    "page": "PAGE",
    "event_name": "EVENT_NAME",
    "event_time": EVENT_TIME
}'

while true; do
    RANDOM_USER=$((RANDOM % 3)) # between 0 and 2
    RANDOM_PAGE=$((RANDOM % 3))
    RANDOM_EVENT=$((RANDOM % 3))

    REQUEST_PAYLOAD=$(echo $PAYLOAD | sed \
        -e "s|USERNAME|${USERNAMES[$RANDOM_USER]}|g" \
        -e "s|PAGE|${PAGES[$RANDOM_PAGE]}|g" \
        -e "s|EVENT_NAME|${EVENT_NAMES[$RANDOM_EVENT]}|g" \
        -e "s|EVENT_TIME|$(date +%s)|g")

    curl -X POST \
        -d "$REQUEST_PAYLOAD" \
        -H 'Content-type: application/json' \
        -w "\n" \
        "http://localhost:3000/event/$TOPIC"

    sleep $DELAY
done
