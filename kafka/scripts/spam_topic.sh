#!/bin/bash
TOPIC=$1
DELAY=$2

[ -z "$TOPIC" -o -z "$DELAY" ] && echo "Usage: spam_topic.sh topic-name delay-time" && exit 1

FIELDS='[{\"name\":\"username\",\"type\":\"string\"},{\"name\":\"page\",\"type\":\"string\"},{\"name\":\"event_name\",\"type\":\"string\"},{\"name\":\"event_time\",\"type\":\"long\"}]'
VALUE_SCHEMA="{\\\"type\\\":\\\"record\\\",\\\"name\\\":\\\"user_event\\\",\\\"fields\\\":$FIELDS}"
KEY_SCHEMA='{\"type\": \"string\"}'
EVENT_TYPES=('click' 'submit' 'checkout')
USER_NAMES=('John', 'Mary', 'Cris')
PAGES=('google.com/users' 'facebook.com/users' 'twitter.com/users')

# Using Kafka REST Proxy API
while true
do
    RANDOM_USER=$((RANDOM % 3)) # between 0 and 2
    RANDOM_EVENT=$((RANDOM % 3))
    RANDOM_PAGE=$((RANDOM % 3))
    NOW=$(date +%s)
    PAYLOAD="{
        \"key_schema\": \"$KEY_SCHEMA\",
        \"value_schema\": \"$VALUE_SCHEMA\",
        \"records\": [
            {
                \"key\": \"`uuidgen`\",
                \"value\": {
                    \"username\": \"${USER_NAMES[$RANDOM_USER]}\",
                    \"event_name\": \"${EVENT_TYPES[$RANDOM_EVENT]}\",
                    \"page\": \"${PAGES[$RANDOM_PAGE]}\",
                    \"event_time\": $NOW
                }
            }
        ]
    }"
    echo $PAYLOAD

    curl -X POST -H "Content-Type: application/vnd.kafka.avro.v2+json" \
        -H "Accept: application/vnd.kafka.v2+json" \
        -w "\n" \
        -d "$PAYLOAD" \
        "http://localhost:8082/topics/$TOPIC"
    sleep $DELAY
done
