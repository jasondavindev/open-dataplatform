#!/bin/bash

docker exec namenode bash -c "hdfs dfs -mkdir -p /kafka/logs; \
hdfs dfs -mkdir -p /kafka/topics; \
hdfs dfs -chown -R appuser /kafka"
