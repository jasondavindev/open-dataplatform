# API Ingestion

## What is

API Ingestion is an application to send events to Kafka using Apache Avro format. The `event` param should be a valid Kafka topic name and the request body should be a valid valid for the schema defined in the schema registry for the passed topic.

## How to use

Primally, must be register the schema on schema registry. For this, starts the [Kafka module](../kafka) and then starts this application.

Calls schema registry subject registration endpoint

```bash
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    --data '{"schema":"{\"type\":\"record\",\"name\":\"Example\",\"fields\":[{\"name\":\"key\",\"type\":\"string\"},{\"name\":\"value\",\"type\":\"string\"}]}"}' \
    http://localhost:8081/subjects/topic-example-value/versions
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

## Development mode

Using the [Nodemon](https://www.npmjs.com/package/nodemon)

```bash
nodemon -w . -e go --exec "sh start.sh"
```
