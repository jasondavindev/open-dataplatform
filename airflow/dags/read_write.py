from airflow import DAG

from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 3, 5),
    "retries": 3,
    "retry_delay": timedelta(seconds=10),
}
dag = DAG(
    'sample_spark',
    default_args=args,
    schedule_interval="0 4 * * *",
    catchup=False,
)

operator = SparkSubmitOperator(
    task_id='read_write_hdfs',
    conn_id='spark',
    application='hdfs://namenode:8020/spark/read_write_hdfs.py',
    total_executor_cores='1',
    executor_cores='1',
    executor_memory='2g',
    num_executors='1',
    name='airflow-spark-example',
    verbose=True,
    driver_memory='1g',
    dag=dag,
)

operator