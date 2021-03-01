FROM openjdk:8-jre-slim

LABEL MAINTAINER="jasondavin.dev@gmail.com"

ARG version=3.3.0

ENV HADOOP_VERSION=$version \
    HADOOP_HOME=/opt/hadoop \
    HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop \
    PATH=$PATH:/opt/hadoop/bin \
    MULTIHOMED_NETWORK=1 \
    CLUSTER_NAME=hadoop \
    HDFS_CONF_dfs_namenode_name_dir=file:///dfs/name \
    HDFS_CONF_dfs_datanode_data_dir=file:///dfs/data \
    USER=hdfs

RUN apt-get update && apt-get install -y curl procps; \
    rm -rf /var/lib/apt/lists/*; \
    curl -SL https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz | tar xvz -C /opt
    
RUN ln -s /opt/hadoop-$HADOOP_VERSION /opt/hadoop; \
    if [ ! -f $HADOOP_CONF_DIR/mapred-site.xml ]; then \
    cp $HADOOP_CONF_DIR/mapred-site.xml.template $HADOOP_CONF_DIR/mapred-site.xml; \
    fi; \
    mkdir -p /var/lib/hadoop/hdfs; \
    groupadd -g 114 -r hadoop; \
    useradd -u 201 --shell /bin/bash -Mr --groups hadoop -d /var/lib/hadoop/hdfs hdfs; \
    mkdir -p /dfs; \
    mkdir -p /opt/hadoop/logs; \
    chown -R hdfs:hadoop /dfs; \
    chown -LR hdfs:hadoop /opt/hadoop

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

USER hdfs

WORKDIR ${HADOOP_HOME}

VOLUME /dfs

EXPOSE 8020 50070 9870

ENTRYPOINT [ "/entrypoint.sh" ]
