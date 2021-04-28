FROM open-dataplatform-hadoop-base:3.2.1

ENV HIVE_VERSION 3.1.2
ENV HIVE_HOME /opt/hive
ENV HIVE_CONF_DIR ${HIVE_HOME}/conf
ENV PATH "${PATH}:${HIVE_HOME}/bin"
ENV HADOOP_CLASSPATH "${HADOOP_CLASSPATH}:${HIVE_HOME}/lib/*"

WORKDIR /opt

RUN wget https://downloads.apache.org/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz; \
    tar -xzvf apache-hive-$HIVE_VERSION-bin.tar.gz; \
    mv apache-hive-$HIVE_VERSION-bin hive; \
    rm apache-hive-$HIVE_VERSION-bin.tar.gz

ENV GUAVA_VERSION 27.0-jre

RUN rm ${HIVE_HOME}/lib/guava*; \
    wget https://repo1.maven.org/maven2/com/google/guava/guava/${GUAVA_VERSION}/guava-${GUAVA_VERSION}.jar -O ${HIVE_HOME}/lib/guava-${GUAVA_VERSION}.jar

ADD entrypoint.sh /entrypoint.sh

RUN mkdir -p ${HIVE_CONF_DIR}; \
    mkdir -p ${HIVE_HOME}/var/log; \
    chmod +x /entrypoint.sh

WORKDIR ${HIVE_HOME}

ENTRYPOINT [ "/entrypoint.sh" ]
