FROM openjdk:8-jre-slim

ENV HADOOP_VERSION 3.2
ENV SPARK_VERSION 3.1.1
ENV TAR_FILE spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
ENV SPARK_HOME /opt/spark
ENV PATH "${PATH}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin"
ENV HADOOP_HOME /opt/hadoop
ENV HADOOP_CONF_DIR ${HADOOP_HOME}/conf

RUN apt update; \
    apt install -y python3 \
    python3-pip \
    wget \
    procps \
    curl; \
    # download spark
    wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/${TAR_FILE}; \
    ln -sL $(which python3) /usr/bin/python

RUN tar -xzvf ${TAR_FILE} -C /opt; \
    ln -sL /opt/${TAR_FILE%.tgz} ${SPARK_HOME}; \
    rm /${TAR_FILE}

WORKDIR ${SPARK_HOME}

ADD entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 7077 6066

# web ui for master and workers respectively
EXPOSE 8080 8081

ENTRYPOINT [ "/entrypoint.sh" ]
