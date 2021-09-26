from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.hooks.webhdfs_hook import WebHDFSHook
import logging
import requests


class HelloOperator(BaseOperator):

    def __init__(
            self,
            name: str,
            **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.hdfs_hook = WebHDFSHook('hdfs_http', 'airflow')

    def execute(self, context):
        message = "Hello {}".format(self.name)
        print(message)
        logging.info("testando")
        data = requests.get(f'http://ingestion-api.dataplatform.svc.cluster.local:3000/records', {
            'count': 1,
            'date': '2021-05-10'
        }).json()
        logging.info(data)
        return message


default_args = {
    "retries": 2,
    "depends_on_past": False,
    "start_date": datetime(2021, 9, 7),
    "retry_delay": timedelta(seconds=10),
}

with DAG(
    dag_id="test",
    default_args=default_args,
    schedule_interval="0 18 * * *",
    catchup=False,
) as dag:
    hello_task = HelloOperator(task_id='sample-task', name='foo_bar')
