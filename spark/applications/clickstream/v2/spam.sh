#!/bin/bash

# on namenode
hdfs dfs -mkdir -p /spark/scripts
hdfs dfs -copyFromLocal v2.py /spark/scripts/v2.py

# on kafkacat
while true; do
    echo "{\"name\":\"$(uuidgen)\",\"age\":$(date +%s)}" | kafkacat -P -t test -b broker-svc.kafka.svc.cluster.local:29092 -c 1
    sleep 0.01
done
