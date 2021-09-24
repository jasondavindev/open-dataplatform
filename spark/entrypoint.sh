#!/bin/bash
SPARK_CLASSPATH="$SPARK_CLASSPATH:${SPARK_HOME}/jars/*"
SPARK_CLASSPATH="$SPARK_HOME/conf:$SPARK_CLASSPATH"

env | grep SPARK_JAVA_OPT_ | sort -t_ -k4 -n | sed 's/[^=]*=\(.*\)/\1/g' > /tmp/java_opts.txt
readarray -t SPARK_EXECUTOR_JAVA_OPTS < /tmp/java_opts.txt

case "$1" in
    master)
        "$SPARK_HOME/bin/spark-class" org.apache.spark.deploy.master.Master \
            -h $SPARK_MASTER_HOST \
            -p $SPARK_MASTER_PORT \
            --webui-port $SPARK_MASTER_WEBUI_PORT
        ;;
    worker)
        "$SPARK_HOME/bin/spark-class" org.apache.spark.deploy.worker.Worker \
            --webui-port $SPARK_WORKER_WEBUI_PORT \
            $SPARK_MASTER_URL
        ;;
    driver)
        shift 1
        "$SPARK_HOME/bin/spark-submit" \
            --conf "spark.driver.bindAddress=$SPARK_DRIVER_BIND_ADDRESS" \
            --deploy-mode client \
            "$@"
        ;;
    executor)
        shift 1
        "$SPARK_HOME/bin/spark-class" \
            "${SPARK_EXECUTOR_JAVA_OPTS[@]}" \
            -Xms$SPARK_EXECUTOR_MEMORY \
            -Xmx$SPARK_EXECUTOR_MEMORY \
            -cp "$SPARK_CLASSPATH:$SPARK_DIST_CLASSPATH" \
            org.apache.spark.executor.CoarseGrainedExecutorBackend \
            --driver-url $SPARK_DRIVER_URL \
            --executor-id $SPARK_EXECUTOR_ID \
            --cores $SPARK_EXECUTOR_CORES \
            --app-id $SPARK_APPLICATION_ID \
            --hostname $SPARK_EXECUTOR_POD_IP \
            --resourceProfileId $SPARK_RESOURCE_PROFILE_ID
        ;;
    *)
        echo "Unkown command"
        exit 1
        ;;
esac
