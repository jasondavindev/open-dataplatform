FROM openjdk:8

ARG HADOOP_VERSION

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    net-tools \
    curl \
    netcat \
    gnupg \
    libsnappy-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

ENV HADOOP_VERSION ${HADOOP_VERSION}
ENV HADOOP_URL https://www.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz

RUN set -x \
    && curl -fSL "$HADOOP_URL" -o /tmp/hadoop.tar.gz \
    && tar -xvf /tmp/hadoop.tar.gz -C /opt/ \
    && mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop \
    && rm /tmp/hadoop.tar.gz*

RUN ln -s /opt/hadoop/etc/hadoop /etc/hadoop

RUN mkdir -p /opt/hadoop/logs; \
    mkdir -p /hadoop-data

ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV HADOOP_MAPRED_HOME ${HADOOP_HOME}
ENV USER=root
ENV PATH $HADOOP_HOME/bin/:$PATH
ENV HADOOP_CLASSPATH "${JAVA_HOME}/lib/tools.jar:${HADOOP_HOME}/share/hadoop/tools/lib/*"

WORKDIR ${HADOOP_HOME}
