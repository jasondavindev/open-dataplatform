#!/bin/bash
if [ "$NODE_TYPE" == "namenode" ]; then
    if [ -z "$CLUSTER_NAME" ]; then
        echo "Cluster name not specified"
        exit 2
    fi

    echo "remove lost+found from $HDFS_NAMENODE_DIR"
    rm -r $HDFS_NAMENODE_DIR/lost+found

    if [ "`ls -A $HDFS_NAMENODE_DIR`" == "" ]; then
        echo "Formatting namenode name directory: $HDFS_NAMENODE_DIR"
        $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME
    fi

    $HADOOP_HOME/bin/hdfs --loglevel INFO,WARN,ERROR,Console --config $HADOOP_CONF_DIR namenode

elif [ "$NODE_TYPE" == "datanode" ]; then
    $HADOOP_HOME/bin/hdfs --loglevel INFO,WARN,ERROR,Console --config $HADOOP_CONF_DIR datanode
else
    echo "Invalid node type"
    exit 1
fi
