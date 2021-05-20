#!/bin/bash

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    -d '{"schema":"{\"type\":\"record\",\"name\":\"User\",\"fields\":[{\"name\":\"name\",\"type\":\"string\"},{\"name\":\"favorite_color\",\"type\":\"string\"}]}"}' \
    http://localhost:8081/subjects/topic-example-value/versions
