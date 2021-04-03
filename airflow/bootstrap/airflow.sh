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

# variables
echo "{
    }" > variables.json

airflow variables import variables.json

# connections
airflow connections add spark --conn-type=spark --conn-host=spark://spark-master:7077 --conn-extra='{"queue": "root.default","master":"spark://spark-master:7077","spark_binary": "spark-submit"}' &
airflow connections add hdfs_http --conn-type=http --conn-host=namenode --conn-port=50070 &
airflow connections add hdfs --conn-type=hdfs --conn-host=namenode --conn-port=8020 &
airflow connections add status_invest_conn --conn-type=http --conn-host=https://statusinvest.com.br/
wait

airflow db upgrade

echo "Environment is ready"
