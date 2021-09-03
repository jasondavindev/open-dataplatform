#!/bin/bash

HADOOP_VERSION=3.2.1
HIVE_VERSION=3.1.2
SPARK_VERSION=3.1.2
AIRFLOW_VERSION=2.1.2

IMAGES_PREFIX="open-dataplatform"

function build_hadoop {
    HADOOP_PATH="$PWD/hadoop/docker/base/"
    docker build -f $HADOOP_PATH/Dockerfile \
        -t "$IMAGES_PREFIX-hadoop-base" \
        --build-arg HADOOP_VERSION=${HADOOP_VERSION} \
        $HADOOP_PATH
}

function build_hdfs {
    HDFS_PATH="$PWD/hadoop/docker/hdfs/"
    docker build -f $HDFS_PATH/Dockerfile \
        -t "$IMAGES_PREFIX-hadoop-hdfs" \
        $HDFS_PATH
}

function build_hive {
    HIVE_PATH="$PWD/hadoop/docker/hive/"
    docker build -f $HIVE_PATH/Dockerfile \
        -t "$IMAGES_PREFIX-hive" \
        --build-arg HIVE_VERSION=$HIVE_VERSION \
        $HIVE_PATH
}

function build_spark {
    SPARK_PATH="$PWD/spark/"
    docker build -f $SPARK_PATH/Dockerfile \
        -t "$IMAGES_PREFIX-spark" \
        --build-arg SPARK_VERSION=$SPARK_VERSION \
        $SPARK_PATH
}

function build_airflow {
    AIRFLOW_PATH="$PWD/airflow/"
    docker build -f $AIRFLOW_PATH/Dockerfile \
        -t "$IMAGES_PREFIX-airflow" \
        --build-arg AIRFLOW_VERSION=$AIRFLOW_VERSION \
        $AIRFLOW_PATH
}

function build_kafka_connect {
    KAFKA_PATH="$PWD/kafka/"
    docker build -f $KAFKA_PATH/connect.Dockerfile \
        -t "$IMAGES_PREFIX-kafka-connect" \
        $KAFKA_PATH
}

build_hadoop
build_hdfs
build_hive
build_spark
build_airflow
build_kafka_connect
