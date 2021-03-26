FROM confluentinc/cp-kafka-connect:6.1.1

WORKDIR /usr/share/java

USER root

RUN yum update -y; \
    yum install -y unzip; \
    wget https://d1i4a15mxbxib1.cloudfront.net/api/plugins/confluentinc/kafka-connect-hdfs/versions/10.0.2/confluentinc-kafka-connect-hdfs-10.0.2.zip; \
    unzip confluentinc-kafka-connect-hdfs-10.0.2.zip; \
    rm -f confluentinc-kafka-connect-hdfs-10.0.2.zip

USER appuser

ENTRYPOINT [ "/etc/confluent/docker/run" ]
