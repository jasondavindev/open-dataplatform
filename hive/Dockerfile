FROM open-dataplatform-hadoop

ENV HIVE_VERSION=3.1.2
ENV APP_HOME /opt

ENV HIVE_HOME ${APP_HOME}/hive
ENV HIVE_FILE apache-hive-$HIVE_VERSION-bin.tar.gz
ENV HIVE_CONF ${HIVE_HOME}/conf
ENV GUAVA_VERSION=27.0-jre

WORKDIR ${APP_HOME}

RUN wget https://downloads.apache.org/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz; \
    tar -xzvf apache-hive-$HIVE_VERSION-bin.tar.gz; \
    mv apache-hive-$HIVE_VERSION-bin hive; \
    rm apache-hive-$HIVE_VERSION-bin.tar.gz; \
    wget https://jdbc.postgresql.org/download/postgresql-9.4.1212.jar; \
    mv postgresql-9.4.1212.jar $HIVE_HOME/lib/postgresql-jdbc.jar; \
    rm ${HIVE_HOME}/lib/guava*; \
    wget https://repo1.maven.org/maven2/com/google/guava/guava/${GUAVA_VERSION}/guava-${GUAVA_VERSION}.jar; \
    mv guava-${GUAVA_VERSION}.jar ${HIVE_HOME}/lib/guava-${GUAVA_VERSION}.jar; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

ENV PATH ${PATH}:${HIVE_HOME}/bin

WORKDIR ${HIVE_HOME}

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 10000 9083 10002

ENTRYPOINT [ "/entrypoint.sh" ]
