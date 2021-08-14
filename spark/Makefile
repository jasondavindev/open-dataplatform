run_script:
	@echo [Running] Spark script ${script}
	@docker exec spark-master\
		/opt/spark/bin/spark-submit \
			--master spark://spark-master:7077 \
			hdfs://namenode:8020/spark/scripts/${script} ${args}

SCRIPTS_PATH = /spark/scripts
FILE_NAME = $$(basename ${file})

import_script: create_spark_scripts_path
	@echo [Importing] Spark script to ${SCRIPTS_PATH}/${FILE_NAME}
	@docker cp ${file} namenode:/tmp/${FILE_NAME}
	@docker exec namenode sh -c "hdfs dfs -copyFromLocal -f \
		/tmp/${FILE_NAME} \
		${SCRIPTS_PATH}/${FILE_NAME}"

create_spark_scripts_path:
	if [ ! -f "${file}" ];then /usr/bin/echo Script file not exist && exit 1;fi
	@echo [Creating] Spark folder
	@docker exec namenode sh -c "hdfs dfs -ls ${SCRIPTS_PATH} || hdfs dfs -mkdir -p ${SCRIPTS_PATH}"
