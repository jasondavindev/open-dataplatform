#!/bin/bash
TOPIC=$1
AVRO=$2

if [ ! -z "$AVRO" ]; then
    ADD_AVRO="-s avro -r schema-registry:8081"
fi

docker run --rm -ti \
    --network=open-dataplatform-network \
    confluentinc/cp-kafkacat bash -c "kafkacat -C -t $TOPIC -b broker:29092 $ADD_AVRO"
