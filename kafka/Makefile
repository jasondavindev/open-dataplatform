.PHONY: consume_topic
consume_topic:
	docker run --rm -ti\
		--network=dataplatform_default\
		confluentinc/cp-kafkacat bash -c "kafkacat -C -t ${topic} -b broker:29092"
