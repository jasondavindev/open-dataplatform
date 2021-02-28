export CORE_CONF_fs_defaultFS=${CORE_CONF_fs_defaultFS:-${HDFS_NAMENODE_URL:-hdfs://`hostname -I`:8020}}

node_type=$1

function check_directory() {
    local path=$1
    local node_type=$2

    namedir=${path#"file://"}
    if [ ! -d $namedir ]; then
        echo "Creating not existing $node_type directory: $namedir"
        mkdir -p $namedir
    fi

    echo $namedir
}

case "$node_type" in
    (namenode)
        shift
        namedir=$(check_directory $HDFS_CONF_dfs_namenode_name_dir namenode)

        if [ "`ls -A $namedir`" == "" ]; then
          echo "Formatting namenode name directory: $namedir"
          $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME
        fi

        $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode $@
      ;;

    (datanode)
      shift
        check_directory $HDFS_CONF_dfs_datanode_data_dir namenode

        $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR datanode $@
      ;;
    (*)
      exec "$@"
      ;;
esac
