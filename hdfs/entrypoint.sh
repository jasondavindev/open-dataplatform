#!/bin/bash
if [ "$IS_MASTER" == "1" -a -z "$(ls /hadoop/hdfs/data)" ];then
  hdfs namenode -format
fi

exec "$@"
