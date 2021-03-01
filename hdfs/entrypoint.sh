#!/bin/bash
DK_HOSTNAME=$(hostname -A)
export CORE_DEFAULT_FS_VALUE=${HDFS_NAMENODE_URL:-`printf "hdfs://%s:8020" $DK_HOSTNAME`}

echo "Replacing core-site defaultFS=$CORE_DEFAULT_FS_VALUE"

sed "s~CORE_DEFAULT_FS_VALUE~${CORE_DEFAULT_FS_VALUE}~g" /tmp/core-site.temp.xml > $HADOOP_CONF_DIR/core-site.xml

node_type=$1

function check_directory() {
    local path=$1
    local node_type=$2

    namedir=${path#"file://"}
    if [ ! -d $namedir ]; then
        echo "Creating not existing $node_type directory: $namedir"
        mkdir -p $namedir
    fi
}

case "$node_type" in
    (namenode)
        shift
        namedir=${HDFS_CONF_dfs_namenode_name_dir#"file://"}
        check_directory $namedir namenode

        if [ "`ls -A $namedir`" == "" ]; then
          echo "Formatting namenode name directory: $namedir"
          $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME
        fi

        $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode $@
      ;;

    (datanode)
      shift
        namedir=${HDFS_CONF_dfs_datanode_data_dir#"file://"}
        check_directory $namedir datanode

        $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR datanode $@
      ;;
    (*)
      exec "$@"
      ;;
esac
