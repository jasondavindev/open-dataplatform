#!/bin/bash
QUERY="CREATE EXTERNAL TABLE IF NOT EXISTS kafka.topic_example (
  key string
)
PARTITIONED BY (value string)
STORED AS PARQUET
LOCATION 'hdfs://namenode:8020/kafka/topics/topic-example';"

docker exec -ti hive bash -c "beeline \
    -u jdbc:hive2://localhost:10000 \
    -e \"$QUERY\""
