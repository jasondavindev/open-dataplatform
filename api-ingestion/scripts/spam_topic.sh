#!/bin/bash
TOPIC=$1
DELAY=$2

[ -z "$TOPIC" -o -z "$DELAY" ] && echo "Usage: spam_topic.sh topic-name delay-time" && exit 1

VALUE_SCHEMA='{\"type\":\"record\",\"name\":\"user_events\",\"fields\":[{\"name\":\"name\",\"type\":\"string\"},{\"name\":\"favorite_color\",\"type\":\"string\"},{\"name\":\"event_time\",\"type\":\"long\"}]}'
KEY_SCHEMA='{\"type\": \"string\"}'
COLORS=('blue' 'green' 'red')

# Using Kafka REST Proxy API
while true
do
    RANDOM_NUMBER=$((RANDOM % 3)) # between 0 and 2
    NOW=$(date +%s)
    PAYLOAD="{
        \"key_schema\": \"$KEY_SCHEMA\",
        \"value_schema\": \"$VALUE_SCHEMA\",
        \"records\": [
            {
                \"key\": \"teste\",
                \"value\": {
                    \"name\": \"`uuidgen`\",
                    \"favorite_color\": \"${COLORS[$RANDOM_NUMBER]}\",
                    \"event_time\": $NOW
                }
            }
        ]
    }"

    curl -X POST -H "Content-Type: application/vnd.kafka.avro.v2+json" \
        -H "Accept: application/vnd.kafka.v2+json" \
        -w "\n" \
        -d "$PAYLOAD" \
        "http://localhost:8082/topics/$TOPIC"
    sleep $DELAY
done
