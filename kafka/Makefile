.PHONY: consume_topic
consume_topic:
	docker run --rm -ti\
		--network=dataplatform_default\
		confluentinc/cp-kafkacat bash -c "kafkacat -C -t ${topic} -b broker:29092 -s avro -r schema-registry:8081"

.PHONY: create_example_schema
create_example_schema:
	@curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json"\
    --data '{"schema":"{\"type\":\"record\",\"name\":\"Example\",\"fields\":[{\"name\":\"Id\",\"type\":\"string\"},{\"name\":\"Type\",\"type\":\"string\"},{\"name\":\"Data\",\"type\":\"string\"},{\"name\":\"Timestamp\",\"type\":\"long\"}]}"}'\
    http://localhost:8081/subjects/test-value/versions
	@curl -X PUT -H "Content-Type: application/json"\
     --data '{"compatibility": "NONE"}'\
     http://localhost:8081/config/test-value
