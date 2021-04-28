FROM open-dataplatform-hadoop-base:3.2.1

RUN mkdir -p /hadoop/dfs/namenode; \
    mkdir -p /hadoop/dfs/datanode

ADD entrypoint.sh /entrypoint.sh

RUN chmod a+x /entrypoint.sh

ENV HDFS_NAMENODE_DIR  /hadoop/dfs/namenode
ENV HDFS_DATANODE_DIR  /hadoop/dfs/datanode

EXPOSE 50070 50075

ENTRYPOINT [ "/entrypoint.sh" ]
