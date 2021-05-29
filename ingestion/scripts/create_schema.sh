#!/bin/bash
TOPIC=$1

[ -z "$TOPIC" ] && echo "Usage script.sh topic-name" && exit 1

FIELDS='[
    {"name":"username","type":"string"},
    {"name":"page","type":"string"},
    {"name":"event_name","type":"string"},
    {"name":"event_time","type":"long"}
]'

FIELDS_X=$(echo $FIELDS | xargs -0)

SCHEMA='{
    "type":"record",
    "name":"TOPIC_NAME",
    "fields": SCHEMA_FIELDS
}'

SCHEMA_X=$(echo $SCHEMA | sed -e "s~SCHEMA_FIELDS~$FIELDS_X~g" -e 's~"~\\\"~g' -e "s~TOPIC_NAME~$TOPIC~g")

PAYLOAD="{\"schema\":\"$SCHEMA_X\"}"

echo "$PAYLOAD"

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    -d "$PAYLOAD" \
    http://localhost:8081/subjects/$TOPIC-value/versions

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    -d '{"schema":"{\"type\":\"string\"}"}' \
    http://localhost:8081/subjects/$TOPIC-key/versions
