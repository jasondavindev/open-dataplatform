FROM open-dataplatform-hdfs

ARG HIVE_VERSION=2.3.8

ENV HIVE_HOME=/opt/hive
ENV HIVE_FILE=apache-hive-$HIVE_VERSION-bin.tar.gz
ENV HIVE_CONF=${HIVE_HOME}/conf
ENV PATH=${PATH}:${HIVE_HOME}/bin

USER root

RUN apt update -yqq; \
    apt install -yqq netcat; \
    curl https://archive.apache.org/dist/hive/hive-$HIVE_VERSION/${HIVE_FILE} -o /tmp/$HIVE_FILE; \
    tar -xzvf /tmp/$HIVE_FILE -C /opt; \
    ln -sL /opt/${HIVE_FILE%.tar.gz} /opt/hive; \
    apt clean; \
    rm -rf /var/lib/apt/lists/*; \
    curl https://jdbc.postgresql.org/download/postgresql-9.4.1212.jar -o $HIVE_HOME/lib/postgresql-jdbc.jar

ENV GUAVA_VERSION=27.0-jre

# remove conflict jars
RUN rm ${HIVE_HOME}/lib/guava-*.jar; \
    curl https://repo1.maven.org/maven2/com/google/guava/guava/${GUAVA_VERSION}/guava-${GUAVA_VERSION}.jar -o ${HIVE_HOME}/lib/guava-${GUAVA_VERSION}.jar

COPY config/* ${HIVE_CONF}/

COPY entrypoint.sh /entrypoint.sh

WORKDIR ${HIVE_HOME}

RUN useradd -s /bin/bash -d ${HIVE_HOME} hive; \
    chown -RL hive:hadoop ${HIVE_HOME}; \
    chmod +x /entrypoint.sh

USER hive

EXPOSE 10000 9083 10002

ENTRYPOINT [ "/entrypoint.sh" ]
