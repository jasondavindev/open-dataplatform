FROM open-dataplatform-hdfs

ARG HIVE_VERSION=3.1.2

ENV HIVE_HOME=/opt/hive
ENV HIVE_FILE=apache-hive-$HIVE_VERSION-bin.tar.gz
ENV HIVE_CONF=${HIVE_HOME}/conf
ENV PATH=${PATH}:${HIVE_HOME}/bin

USER root

RUN curl https://archive.apache.org/dist/hive/hive-$HIVE_VERSION/${HIVE_FILE} -o /tmp/$HIVE_FILE; \
    tar -xzvf /tmp/$HIVE_FILE -C /opt; \
    ln -sL /opt/${HIVE_FILE%.tar.gz} /opt/hive; \
    apt clean; \
    rm -rf /var/lib/apt/lists/*; \
    # remove conflict jars
    rm ${HIVE_HOME}/lib/guava-19.0.jar; \
    cp ${HADOOP_HOME}/share/hadoop/hdfs/lib/guava-27.0-jre.jar ${HIVE_HOME}/lib/

COPY config/* ${HIVE_CONF}/

WORKDIR ${HIVE_HOME}

RUN useradd -ms /bin/bash -d ${HIVE_HOME} hive

USER hive

EXPOSE 10000 9083

ENTRYPOINT [ "" ]