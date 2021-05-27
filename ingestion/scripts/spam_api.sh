#!/bin/bash
TOPIC=$1
DELAY=$2

[ -z "$TOPIC" -o -z "$DELAY" ] && echo "Usage script.sh topic-name delay" && exit 1

USERNAMES=('John' 'Mary' 'Cris')
COLORS=('black' 'red' 'blue')

PAYLOAD='{
    "name": "USERNAME",
    "favorite_color": "COLOR"
}'

while true; do
    RANDOM_USER=$((RANDOM % 3)) # between 0 and 2
    RANDOM_COLOR=$((RANDOM % 3))

    REQUEST_PAYLOAD=$(echo $PAYLOAD | sed -e "s|USERNAME|${USERNAMES[$RANDOM_USER]}|g" -e "s|COLOR|${COLORS[$RANDOM_COLOR]}|g")

    curl -X POST \
        -d "$REQUEST_PAYLOAD" \
        -H 'Content-type: application/json' \
        -w "\n" \
        "http://localhost:3000/event/$TOPIC"

    sleep $DELAY
done
