# Kafka

In this module, is provided the Kafka broker, zookeeper, schema registry and a connector to stream kafka events to HDFS.

## How to run

Start up the containers

```bash
docker-compose up
```

## Listen topics

To listen topics, use the Makefile command

```
make consume_topic topic=TOPIC_NAME
```

This uses the Kafkacat confluent image.

## Create new topic

To send events to new topic, create the schema on schema registry. In the Makefile there are a command to create a sample schema.

By convention topics are created in Avro format.
