import os
from datetime import datetime, timedelta, date
from airflow.models import DAG
from dataplatform.operators.status_invest.status_invest_to_hdfs_operator import StatusInvestToHDFSOperator
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
    HDFS_URI = os.getenv('HDFS_HOST')
    date = '{{ds}}'

    stocks = StatusInvestToHDFSOperator(
        task_id='stocks_to_hdfs',
        dt=date,
        category_type='stocks'
    )

    stocks_json_to_parquet = DockerSparkSubmitOperator(
        task_id='stocks_json_to_parquet',
        application="/utils/json_to_parquet.py",
        application_args=[
            '--json-files-path', f"{HDFS_URI}/user/hive/warehouse/raw/status_invest/stocks/dt={date}",
            '--database', 'status_invest',
            '--table', 'stocks',
            '--hdfs-uri', HDFS_URI,
            '--date', date,
            '--partitions', 'date'
        ],
        executor_memory="4GB"
    )

    best_stocks = DockerSparkSubmitOperator(
        task_id="best_stocks",
        application="/best_stocks.py",
        application_args=[
            '--from-database', 'status_invest',
            '--from-table', 'stocks',
            '--to-database', 'status_invest',
            '--to-table', 'best_stocks',
            '--hdfs-uri', HDFS_URI,
        ],
        executor_memory="4GB"
    )

    stocks_historical = DockerSparkSubmitOperator(
        task_id="stocks_historical",
        application="/stocks_historical.py",
        application_args=[
            '--stocks-database', 'status_invest',
            '--stocks-table', 'stocks',
            '--historical-database', 'status_invest',
            '--historical-table', 'stocks_historical',
            '--hdfs-uri', HDFS_URI,
        ],
        executor_memory="4GB"
    )

    fiis = StatusInvestToHDFSOperator(
        task_id='fiis_to_hdfs',
        dt=date,
        category_type='fiis'
    )

    fiis_json_to_parquet = DockerSparkSubmitOperator(
        task_id='fiis_json_to_parquet',
        application="/utils/json_to_parquet.py",
        application_args=[
            '--json-files-path', f"{HDFS_URI}/user/hive/warehouse/raw/status_invest/fiis/dt={date}",
            '--database', 'status_invest',
            '--table', 'fiis',
            '--hdfs-uri', HDFS_URI,
            '--date', date,
            '--partitions', 'date'
        ],
        executor_memory="4GB"
    )

    stocks >> stocks_json_to_parquet >> [best_stocks, stocks_historical]
    fiis >> fiis_json_to_parquet
