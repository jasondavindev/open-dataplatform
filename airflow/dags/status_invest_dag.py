from datetime import datetime, timedelta, date
from airflow.models import DAG
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from dataplatform.operators.status_invest.stocks_to_hdfs_operator import StocksToHDFSOperator
from dataplatform.operators.spark.json_to_parquet_operator import JsonToParquetOperator
from dataplatform.operators.spark.docker_spark_submit_operator import DockerSparkSubmitOperator

default_args = {
    "retries": 4,
    "depends_on_past": False,
    "start_date": datetime(2021, 4, 21),
    "retry_delay": timedelta(seconds=10),
}

with DAG(
    dag_id="status_invest",
    default_args=default_args,
    schedule_interval="0 4 * * *",
    catchup=False,
) as dag:
    date = str(date.today())

    stocks = StocksToHDFSOperator(task_id='stocks_to_hdfs')

    json_to_parquet = JsonToParquetOperator(
        task_id='json_to_parquet',
        conn_id='spark',
        name='json_to_parquet',
        json_files_path=f"/airflow/status_invest/dt={date}/{date}.json",
        hive_database='status_invest',
        hive_table='stocks')

    best_stocks = DockerSparkSubmitOperator(
        task_id="best_stocks",
        application="/scripts/spark/best_stocks.py",
        conn_id='spark',
        application_args=[
            '--from-database', 'status_invest',
            '--from-table', 'stocks',
            '--to-database', 'status_invest',
            '--to-table', 'best_stocks',
            '--hdfs-uri', 'hdfs://namenode:8020',
        ],
    )

    stocks >> json_to_parquet >> best_stocks
