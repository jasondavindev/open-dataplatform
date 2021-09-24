#!/bin/bash
SPARK_CLASSPATH="$SPARK_CLASSPATH:${SPARK_HOME}/jars/*"
env | grep SPARK_JAVA_OPT_ | sort -t_ -k4 -n | sed 's/[^=]*=\(.*\)/\1/g' > /tmp/java_opts.txt
readarray -t SPARK_EXECUTOR_JAVA_OPTS < /tmp/java_opts.txt

if [ -n "$SPARK_EXTRA_CLASSPATH" ]; then
  SPARK_CLASSPATH="$SPARK_CLASSPATH:$SPARK_EXTRA_CLASSPATH"
fi

if ! [ -z ${PYSPARK_PYTHON+x} ]; then
    export PYSPARK_PYTHON
fi
if ! [ -z ${PYSPARK_DRIVER_PYTHON+x} ]; then
    export PYSPARK_DRIVER_PYTHON
fi

# If HADOOP_HOME is set and SPARK_DIST_CLASSPATH is not set, set it here so Hadoop jars are available to the executor.
# It does not set SPARK_DIST_CLASSPATH if already set, to avoid overriding customizations of this value from elsewhere e.g. Docker/K8s.
if [ -n "${HADOOP_HOME}"  ] && [ -z "${SPARK_DIST_CLASSPATH}"  ]; then
  export SPARK_DIST_CLASSPATH="$($HADOOP_HOME/bin/hadoop classpath)"
fi

if ! [ -z ${HADOOP_CONF_DIR+x} ]; then
  SPARK_CLASSPATH="$HADOOP_CONF_DIR:$SPARK_CLASSPATH";
fi

if ! [ -z ${SPARK_CONF_DIR+x} ]; then
  SPARK_CLASSPATH="$SPARK_CONF_DIR:$SPARK_CLASSPATH";
elif ! [ -z ${SPARK_HOME+x} ]; then
  SPARK_CLASSPATH="$SPARK_HOME/conf:$SPARK_CLASSPATH";
fi

case "$1" in
  driver)
    shift 1
    CMD=(
      "$SPARK_HOME/bin/spark-submit"
      --conf "spark.driver.bindAddress=$SPARK_DRIVER_BIND_ADDRESS"
      --deploy-mode client
      "$@"
    )
    ;;
  executor)
    shift 1
    CMD=(
      ${JAVA_HOME}/bin/java
      "${SPARK_EXECUTOR_JAVA_OPTS[@]}"
      -Xms$SPARK_EXECUTOR_MEMORY
      -Xmx$SPARK_EXECUTOR_MEMORY
      -cp "$SPARK_CLASSPATH:$SPARK_DIST_CLASSPATH"
      org.apache.spark.scheduler.cluster.k8s.KubernetesExecutorBackend
      --driver-url $SPARK_DRIVER_URL
      --executor-id $SPARK_EXECUTOR_ID
      --cores $SPARK_EXECUTOR_CORES
      --app-id $SPARK_APPLICATION_ID
      --hostname $SPARK_EXECUTOR_POD_IP
      --resourceProfileId $SPARK_RESOURCE_PROFILE_ID
      --podName $SPARK_EXECUTOR_POD_NAME
    )
    ;;

  *)
    echo "Non-spark-on-k8s command provided, proceeding in pass-through mode..."
    CMD=("$@")
    ;;
esac

exec "${CMD[@]}"