#!/bin/bash

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    --data '{"schema":"{\"type\":\"record\",\"name\":\"Example\",\"fields\":[{\"name\":\"key\",\"type\":\"string\"},{\"name\":\"value\",\"type\":\"string\"}]}"}' \
    http://localhost:8081/subjects/topic-example-value/versions
