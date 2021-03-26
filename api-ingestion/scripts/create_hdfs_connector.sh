curl -i -X PUT http://localhost:8083/connectors/SINK_HDFS/config \
    -H "Content-Type: application/json" \
    -d '{
        "connector.class":"io.confluent.connect.hdfs.HdfsSinkConnector",
        "tasks.max": 3,
        "topics":"topic-example",
        "flush.size": 10,
        "bootstrap.servers": "broker:29092",
        "hdfs.url": "hdfs://namenode:8020",
        "format.class": "io.confluent.connect.hdfs.parquet.ParquetFormat",
        "value.converter": "io.confluent.connect.avro.AvroConverter",
        "value.converter.schema.registry.url": "http://schema-registry:8081",
        "topics.dir": "/kafka/topics",
        "logs.dir": "/kafka/logs",
        "partitioner.class": "io.confluent.connect.storage.partitioner.FieldPartitioner",
        "partition.field.name": "value"
    }'
