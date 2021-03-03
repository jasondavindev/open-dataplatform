#!/bin/bash

SPARK_COMMAND="$1"

case "$SPARK_COMMAND" in
    master)
        echo ">> Try to start Spark Master <<"
        $SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master \
            -h $SPARK_MASTER_HOST \
            -p $SPARK_MASTER_PORT \
            --webui-port $SPARK_MASTER_WEBUI_PORT
        ;;
    worker)
        echo ">> Try to start Spark Worker <<"
        $SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker \
            --webui-port $SPARK_WORKER_WEBUI_PORT \
            $SPARK_MASTER_URL
        ;;
    *)
        echo "Unkown command"
        exit 1
        ;;
esac
