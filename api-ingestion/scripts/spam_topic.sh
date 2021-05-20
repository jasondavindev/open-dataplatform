#!/bin/bash
TOPIC=$1
DELAY=$2

[ -z "$TOPIC" -o -z "$DELAY" ] && echo "Usage: spam_topic.sh topic-name delay-time" && exit 1


while true
do
    PAYLOAD="{ \"key_schema_id\": 2, \"value_schema_id\": \"1\", \"records\": [{\"key\":\"`uuidgen`\",\"value\":{\"name\":\"`uuidgen`\",\"favorite_color\":\"blue\"}}]}"
    curl -X POST -H "Content-Type: application/vnd.kafka.avro.v2+json" \
        -H "Accept: application/vnd.kafka.v2+json" \
        -w "\n" \
        -d "$PAYLOAD" \
        "http://localhost:8082/topics/$TOPIC"
    sleep $DELAY
done
