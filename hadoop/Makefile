dk_prefix = docker exec namenode hdfs dfs

ls:
	${dk_prefix} -ls ${dir}

mkdir:
	${dk_prefix} -mkdir ${flags} ${dir}

rm:
	${dk_prefix} -rm ${dir}

cat:
	${dk_prefix} -cat ${dir}

chown:
	${dk_prefix} -chown ${flags} ${user} ${dir}

cpFromLocal:
	${dk_prefix} -copyFromLocal ${source} ${target}
