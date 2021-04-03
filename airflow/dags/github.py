from airflow import DAG
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta
import requests
from hdfs import InsecureClient
from json import dump, dumps
from dataplatform.operators.github.github_operator import GitHubToHDFSOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

HDFS_URI = 'hdfs://namenode:8020'

default_args = {
    "retries": 1,
    "depends_on_past": False,
    "start_date": datetime(2020, 3, 5)
}

with DAG(
    dag_id="github",
    default_args=default_args,
    schedule_interval="0 4 * * *",
    catchup=False,
) as dag:
    git_to_hdfs = GitHubToHDFSOperator(
        profile="toledompm",
        task_id="github_profile",
        conn_id="hdfs_http"
    )

    spark_operator = SparkSubmitOperator(
        application=f"{HDFS_URI}/spark/scripts/read_file.py",
        task_id="read_github_from_hdfs",
        conn_id="spark",
        name="read_github_from_hdfs",
        application_args=[
            '--namenode', f"{HDFS_URI}",
            '--file', '/spark/2021-04-02'
        ])

    git_to_hdfs >> spark_operator
