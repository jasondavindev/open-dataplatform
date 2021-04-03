from datetime import datetime, timedelta
from airflow.models import DAG
from dataplatform.operators.status_invest.stocks_to_hdfs_operator import StocksToHDFSOperator
from dataplatform.operators.spark.json_to_parquet_operator import JsonToParquetOperator

default_args = {
    "retries": 4,
    "depends_on_past": False,
    "start_date": datetime(2020, 4, 1),
    "retry_delay": timedelta(seconds=10),
}

with DAG(
    dag_id="status_invest",
    default_args=default_args,
    schedule_interval="0 4 * * *",
    catchup=False,
) as dag:
    stocks = StocksToHDFSOperator(task_id='stocks_to_hdfs')
    json_to_parquet = JsonToParquetOperator(
        task_id='json_to_parquet',
        conn_id='spark',
        name='json_to_parquet',
        json_files_path='/airflow/status_invest/dt=2021-04-02/2021-04-02.json',
        hive_database='status_invest',
        hive_table='stocks')

    stocks >> json_to_parquet
