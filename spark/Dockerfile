FROM openjdk:8-jre-slim

LABEL MAINTAINER="jasondavin.dev@gmail.com"

ARG hadoop_version=3.2
ARG spark_version=3.1.1

ENV HADOOP_VERSION=${hadoop_version}
ENV SPARK_VERSION=${spark_version}
ENV TAR_FILE=spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

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
    ln -sL /opt/${TAR_FILE%.tgz} /opt/spark; \
    rm /${TAR_FILE}

WORKDIR /opt/spark

ENV SPARK_HOME=/opt/spark
ENV PATH="${PATH}:${SPARK_HOME}/bin"

# hadoop setup

ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=${HADOOP_HOME}/conf

RUN mkdir -p ${HADOOP_CONF_DIR}

COPY config/* ${HADOOP_CONF_DIR}/

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh; \
    groupadd -g 114 -r hadoop; \
    useradd -u 201 --shell /bin/bash -Mr --groups hadoop -d /opt/spark spark; \
    chown -LR spark:hadoop /opt/spark

USER spark

EXPOSE 7077 6066

# web ui for master and workers respectively
EXPOSE 8080 8081

ENTRYPOINT [ "/entrypoint.sh" ]
