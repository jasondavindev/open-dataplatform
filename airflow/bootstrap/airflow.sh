TRY_LOOP=5

wait_for_port() {
  local name="$1" host="$2" port="$3"
  local j=0
  while ! nc -z "$host" "$port" >/dev/null 2>&1 < /dev/null; do
    j=$((j+1))
    if [ $j -ge $TRY_LOOP ]; then
      echo >&2 "$(date) - $host:$port still not reachable, giving up"
      exit 1
    fi
    echo "$(date) - waiting for $name... $j/$TRY_LOOP"
    sleep 5
  done
}

wait_for_port "Postgres" ${POSTGRES_HOST} ${POSTGRES_PORT}

airflow db init

# connections
airflow connections delete spark
airflow connections delete hdfs_http
airflow connections delete hdfs
airflow connections delete status_invest_conn
airflow connections delete spark-cluster

airflow connections add spark --conn-type=spark --conn-host=spark://spark-master:7077 --conn-extra='{"queue": "root.default","spark_binary": "spark-submit"}' &
airflow connections add hdfs_http --conn-type=http --conn-host=$HDFS_HOST --conn-port=50070 &
airflow connections add hdfs --conn-type=hdfs --conn-host=$HDFS_HOST --conn-port=$HDFS_PORT &
airflow connections add status_invest_conn --conn-type=http --conn-host=https://statusinvest.com.br &
airflow connections add spark-cluster --conn-type=spark --conn-host=k8s://https://$CONTROL_PLANE_IP:6443 --conn-extra='{"queue": "root.default","spark_binary": "spark-submit","deploy-mode":"cluster"}' &
airflow users create --username admin --firstname Open --lastname Dataplatform --role Admin --password admin --email admin@example.org &
wait

airflow db upgrade

echo "Environment is ready"
