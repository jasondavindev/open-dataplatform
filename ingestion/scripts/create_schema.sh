#!/bin/bash
TOPIC=$1

[ -z "$TOPIC" ] && echo "Usage script.sh topic-name" && exit 1

FIELDS='[
    {"name":"name","type":"string"},
    {"name":"favorite_color","type":"string"}
]'

FIELDS_X=$(echo $FIELDS | xargs -0)

SCHEMA='{
    "type":"record",
    "name":"Clickstream",
    "fields": SCHEMA_FIELDS
}'
SCHEMA_X=$(echo $SCHEMA | sed -e "s~SCHEMA_FIELDS~$FIELDS_X~g" -e 's~"~\\\"~g')

PAYLOAD="{\"schema\":\"$SCHEMA_X\"}"

echo "$PAYLOAD"

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    -d "$PAYLOAD" \
    http://localhost:8081/subjects/$TOPIC/versions
