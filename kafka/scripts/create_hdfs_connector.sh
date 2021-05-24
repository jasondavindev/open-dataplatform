#!/bin/bash

curl -i -X PUT http://localhost:8083/connectors/SINK_HDFS/config \
    -H "Content-Type: application/json" \
    -d '{
            "connector.class":"io.confluent.connect.hdfs.HdfsSinkConnector",
            "tasks.max": 1,
            "topics":"topic-example",
            "flush.size": 100,
            "bootstrap.servers": "broker:29092",
            "hdfs.url": "hdfs://namenode:8020",
            "format.class": "io.confluent.connect.hdfs.parquet.ParquetFormat",
            "value.converter": "io.confluent.connect.avro.AvroConverter",
            "value.converter.schema.registry.url": "http://schema-registry:8081",
            "topics.dir": "/user/hive/warehouse/bronze/dumping",
            "logs.dir": "/user/hive/warehouse/logs",
            "partitioner.class": "io.confluent.connect.storage.partitioner.FieldPartitioner",
            "partition.field.name": "value",
            "hive.integration": true,
            "hive.metastore.uris": "thrift://hive-metastore:9083",
            "schema.compatibility": "BACKWARD",
            "hive.database": "dumping"
        }'
