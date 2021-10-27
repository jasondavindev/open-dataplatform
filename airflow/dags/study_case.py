import os
from datetime import datetime, timedelta, date
from airflow.models import DAG
from dataplatform.operators.spark.docker_spark_submit_operator import DockerSparkSubmitOperator
from dataplatform.operators.study_case.study_case_operator import StudyCaseOperator

default_args = {
    "retries": 2,
    "depends_on_past": False,
    "start_date": datetime(2021, 9, 7),
    "retry_delay": timedelta(seconds=10),
}

with DAG(
    dag_id="study_case",
    default_args=default_args,
    schedule_interval="0 18 * * *",
    catchup=False,
) as dag:
    HDFS_URI = f"hdfs://{os.getenv('HDFS_HOST')}:{os.getenv('HDFS_PORT')}"
    date = '{{ds}}'

    insights = StudyCaseOperator(
        task_id='insights_to_hdfs',
        dt=date,
        count=30
    )

    insights_json_to_parquet = DockerSparkSubmitOperator(
        task_id='insights_json_to_parquet',
        application="/utils/json_to_parquet.py",
        application_args=[
            '--json-files-path', f"{HDFS_URI}/user/hive/warehouse/raw/study_case/insights/dt={date}",
            '--database', 'study_case',
            '--table', 'insights',
            '--hdfs-uri', HDFS_URI,
            '--date', date,
            '--partitions', 'date'
        ],
        executor_memory="4GB",
        executor_cores="2",
    )

    group_insights = DockerSparkSubmitOperator(
        task_id='group_insights',
        application="/study_case_transform.py",
        application_args=[
            '--db', 'study_case',
            '--table', 'grouped_insights',
            '--hdfs-uri', HDFS_URI,
            '--date', date
        ],
        executor_memory="4GB",
        executor_cores="2"
    )

    insights >> insights_json_to_parquet >> group_insights
