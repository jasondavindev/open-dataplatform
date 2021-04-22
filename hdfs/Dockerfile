FROM openjdk:8

ENV APP_HOME /opt
ENV HADOOP_VERSION 3.3.0
ENV HADOOP_HOME ${APP_HOME}/hadoop
ENV HADOOP_CONF_DIR /etc/hadoop

RUN apt-get update && apt-get install -y wget netcat curl procps; \
    rm -rf /var/lib/apt/lists/*; \
    wget http://www.eu.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz; \
    tar -xzvf hadoop-$HADOOP_VERSION.tar.gz; \
    mv hadoop-$HADOOP_VERSION ${HADOOP_HOME}; \
    rm hadoop-$HADOOP_VERSION.tar.gz

RUN mkdir -p /hadoop/hdfs/name; \
    mkdir -p /hadoop/hdfs/data; \
    mkdir -p ${HADOOP_CONF_DIR}

ENV PATH $PATH:${HADOOP_HOME}/bin
ENV USER root

ADD entrypoint.sh /entrypoint.sh
ADD config/core-site.xml ${HADOOP_CONF_DIR}
ADD config/hdfs-site.xml ${HADOOP_CONF_DIR}

RUN chmod +x /entrypoint.sh

WORKDIR ${HADOOP_HOME}

EXPOSE 8020 50070 50075

ENTRYPOINT [ "/entrypoint.sh" ]
