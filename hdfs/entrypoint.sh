#!/bin/bash
if [ "$IS_MASTER" == "1" -a -z "$(ls /hadoop/hdfs/name)" ];then
  hdfs namenode -format
fi

exec "$@"
