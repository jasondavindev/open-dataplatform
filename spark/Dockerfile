FROM openjdk:8

ARG SPARK_VERSION=3.1.2

ENV SPARK_VERSION ${SPARK_VERSION}
ENV HADOOP_VERSION 3.2
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
    ln -sL $(which python3) /usr/bin/python; \
    python3 -m pip install requests

RUN tar -xzvf ${TAR_FILE} -C /opt; \
    ln -sL /opt/${TAR_FILE%.tgz} ${SPARK_HOME}; \
    rm /${TAR_FILE}

WORKDIR ${SPARK_HOME}

# install jars
RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-avro_2.12/3.1.1/spark-avro_2.12-3.1.1.jar; \
    wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.1.1/spark-sql-kafka-0-10_2.12-3.1.1.jar; \
    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.6.0/kafka-clients-2.6.0.jar; \
    wget https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.1.1/spark-token-provider-kafka-0-10_2.12-3.1.1.jar; \
    wget https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.6.2/commons-pool2-2.6.2.jar; \
    mv spark-avro_2.12-3.1.1.jar ${SPARK_HOME}/jars/spark-avro_2.12-3.1.1.jar; \
    mv spark-sql-kafka-0-10_2.12-3.1.1.jar ${SPARK_HOME}/jars/spark-sql-kafka-0-10_2.12-3.1.1.jar; \
    mv kafka-clients-2.6.0.jar ${SPARK_HOME}/jars/kafka-clients-2.6.0.jar; \
    mv spark-token-provider-kafka-0-10_2.12-3.1.1.jar ${SPARK_HOME}/jars/spark-token-provider-kafka-0-10_2.12-3.1.1.jar; \
    mv commons-pool2-2.6.2.jar ${SPARK_HOME}/jars/commons-pool2-2.6.2.jar

ADD entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 7077 4040

ENTRYPOINT [ "/entrypoint.sh" ]
