#!/bin/bash
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker \
            --webui-port $SPARK_WORKER_WEBUI_PORT \
            $SPARK_MASTER_URL &

spark-submit \
    --master \
    spark://spark-master:7077 \
    /apps/clickstream.py \
    --topic \
    appclickstream \
    --table-path \
    /spark/clickstream
