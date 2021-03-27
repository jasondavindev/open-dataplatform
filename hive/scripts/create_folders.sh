#!/bin/bash
docker exec namenode bash -c "hdfs dfs -mkdir /tmp; \
hdfs dfs -chmod -R 777 /tmp; \
hdfs dfs -mkdir -p /user/hive/warehouse; \
hdfs dfs -chown -R hive /user/hive/warehouse"

