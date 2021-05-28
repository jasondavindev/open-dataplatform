#!/bin/bash
CONNECT_NAME=$1
TOPICS=$2
FIELD_PARTITION=$3

[ -z "$TOPICS" -o -z "$FIELD_PARTITION" ] && echo "Usage: create_hdfs_connector.sh sink-hdfs topic-1,topic-2,topic-3 field-partition" && exit 1

PAYLOAD='{
            "connector.class":"io.confluent.connect.hdfs.HdfsSinkConnector",
            "tasks.max": 1,
            "topics":"TOPICS_ENV",
            "flush.size": 100,
            "bootstrap.servers": "broker:29092",
            "hdfs.url": "hdfs://namenode:8020",
            "format.class": "io.confluent.connect.hdfs.parquet.ParquetFormat",
            "value.converter": "io.confluent.connect.avro.AvroConverter",
            "value.converter.schema.registry.url": "http://schema-registry:8081",
            "topics.dir": "/user/hive/warehouse/bronze/dumping",
            "logs.dir": "/user/hive/warehouse/logs",
            "partitioner.class": "io.confluent.connect.storage.partitioner.FieldPartitioner",
            "partition.field.name": "FIELD_PARTITION",
            "hive.integration": true,
            "hive.metastore.uris": "thrift://hive-metastore:9083",
            "schema.compatibility": "BACKWARD",
            "hive.database": "dumping"
        }'

PAYLOAD=$(echo $PAYLOAD | sed -e "s|TOPICS_ENV|$TOPICS|g" -e "s|FIELD_PARTITION|$FIELD_PARTITION|g")

echo "$PAYLOAD"

curl -i -X PUT "http://localhost:8083/connectors/$CONNECT_NAME/config" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    -w "\n"
