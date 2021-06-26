# USE HADOOP 3.2.1 by default

build_base:
	docker build -f docker/base/Dockerfile -t open-dataplatform-hadoop-base:${version} --build-arg HADOOP_VERSION=${version} ./docker/base

build_hdfs: build_base
	docker build -f docker/hdfs/Dockerfile -t open-dataplatform-hadoop-hdfs:${hdfs_version} --build-arg HADOOP_VERSION=${hdfs_version} ./docker/hdfs

build_hive: build_base
	docker build -f docker/hive/Dockerfile -t open-dataplatform-hadoop-hive:${hive_version} --build-arg HADOOP_VERSION=${hive_version} ./docker/hive
