# Airflow

To run the Airflow setup, runs `docker-compose up` and await for the containers.

## Running Spark application files in HDFS host

To run DAGs executing spark application files hosted in HDFS container, it is necessary move the script file to `namenode` container, below

```bash
docker cp script_file.py namenode:/tmp/script_file.py
```

Use the make script to copy file container to HDFS file system

```bash
make -f ../hdfs/cpFromLocal source=/tmp/script_file.py target=/airflow/script_file.py
```

## Writing in HDFS files

Because the airflow runs the Spark (spark-submit) as the `airflow` user, it is required create the `airflow` user on the namenode container. Create airflow directory then give permissions

```bash
make -f ../hdfs/Makefile mkdir dir=/airflow # create airflow folder
make -f ../hdfs/Makefile chown flags=-LR dir=/airflow user=airflow # make the owner recursively
```

Now is possible read and write files in HDFS with airflow DAGs.
