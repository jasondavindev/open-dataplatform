# API Ingestion

## What is

API Ingestion is an application to send events to Kafka using Apache Avro format. The `event` param should be a valid Kafka topic name and the request body should be a valid valid for the schema defined in the schema registry for the passed topic.

## How to use

Primally, must be register the schema on schema registry. For this, starts the [Kafka module](../kafka) and then starts this application.

Calls schema registry subject registration endpoint

```bash
sh create_topic_example_schema.sh
```

And then calls the api to send events to Kafka

```bash
curl -X POST localhost:7777/event/topic-example -d  \
'{"key":"a key","value":"the value"}' \
-H 'Content-Type: application/json'
```

To view the topic events, go to the [Kafka Makefile](../kafka/Makefile) and calls

```bash
make consume_topic topic=topic-example
```

## Data stream to HDFS

In the Kafka modules, has been created a Kafka Connect to transfer data from Kafka topics to HDFS. The format used in the flow is Apache Avro (from Kafka) to Apache Parquet (to HDFS).

To create complete setup, it's required run the scripts below

```bash
sh create_topic_example_schema.sh # creates the schema on schmea registry
sh create_kafka_folders.sh # creates the necessary folders on HDFS
sh create_hdfs_connector.sh # instantiate the HDFS connector to stream kafka data to HDFS
```

And then, calls the API to send events.
