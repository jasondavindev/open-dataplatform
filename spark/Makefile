submit-pi:
	docker run --rm\
		--entrypoint ""\
		--network=spark_default\
		open-dataplatform-spark\
		/opt/spark/bin/spark-submit \
			--master spark://spark-master:7077 \
			examples/src/main/python/pi.py 100


SCRIPTS_PATH = /spark/scripts
FILE_NAME = $$(basename ${file})

import_script: create_spark_scripts_path
	@docker cp ${file} namenode:/tmp/${FILE_NAME}
	@docker exec namenode sh -c "hdfs dfs -copyFromLocal -f \
		/tmp/${FILE_NAME} \
		${SCRIPTS_PATH}/${FILE_NAME}"

create_spark_scripts_path:
	$(MAKE) -C ../hdfs ls dir=${SCRIPTS_PATH} || $(MAKE) -C ../hdfs mkdir flags=-p dir=${SCRIPTS_PATH}
