submit-pi:
	docker run --rm\
		--entrypoint ""\
		--network=spark_default\
		open-dataplatform-spark\
		/opt/spark/bin/spark-submit \
			--master spark://spark-master:7077 \
			examples/src/main/python/pi.py 100