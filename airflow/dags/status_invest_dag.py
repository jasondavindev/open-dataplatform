from datetime import datetime, timedelta, date
from airflow.models import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from dataplatform.operators.status_invest.stocks_to_hdfs_operator import StocksToHDFSOperator
from dataplatform.operators.spark.docker_spark_submit_operator import DockerSparkSubmitOperator

default_args = {
    "retries": 4,
    "depends_on_past": False,
    "start_date": datetime(2021, 4, 21),
    "retry_delay": timedelta(seconds=10),
}


def hdfs_uri():
    hook = BaseHook().get_connection('hdfs')
    return f"hdfs://{hook.host}:{hook.port}"


with DAG(
    dag_id="status_invest",
    default_args=default_args,
    schedule_interval="0 4 * * *",
    catchup=False,
) as dag:
    date = str(date.today())

    stocks = StocksToHDFSOperator(task_id='stocks_to_hdfs')

    json_to_parquet = DockerSparkSubmitOperator(
        task_id='json_to_parquet',
        application="/scripts/spark/utils/json_to_parquet.py",
        conn_id='spark',
        application_args=[
            '--json-files-path', f"/airflow/status_invest/dt={date}",
            '--database', 'status_invest',
            '--table', 'stocks',
            '--hdfs-uri', hdfs_uri()
        ]
    )

    best_stocks = DockerSparkSubmitOperator(
        task_id="best_stocks",
        application="/scripts/spark/best_stocks.py",
        conn_id='spark',
        application_args=[
            '--from-database', 'status_invest',
            '--from-table', 'stocks',
            '--to-database', 'status_invest',
            '--to-table', 'best_stocks',
            '--hdfs-uri', hdfs_uri(),
        ],
    )

    stocks >> json_to_parquet >> best_stocks
