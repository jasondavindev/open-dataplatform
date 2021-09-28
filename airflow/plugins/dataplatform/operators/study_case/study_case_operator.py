import json
import requests
import os

from airflow.models.baseoperator import BaseOperator
from airflow.hooks.webhdfs_hook import WebHDFSHook


class StudyCaseOperator(BaseOperator):
    template_fields = ['dt']

    def __init__(
            self,
            dt=None,
            count=30,
            hdfs_conn_id='hdfs_http',
            *args,
            **kwargs):
        self.hdfs_hook = WebHDFSHook(hdfs_conn_id, 'airflow')
        self.dt = dt
        self.count = count
        self.ingestion_api_url = os.getenv('INGESTION_API_URL')

        super().__init__(*args, **kwargs)

    def _get_insights(self):
        return requests.get(f'{self.ingestion_api_url}/records', {
            'count': self.count,
            'date': self.dt
        }).json()

    def execute(self, context):
        data = self._get_insights()
        print(data)

        with open('/tmp/result.json', 'w') as outfile:
            json.dump(data, outfile)

        return self.hdfs_hook.load_file(
            "/tmp/result.json",
            f"/user/hive/warehouse/raw/study_case/insights/dt={self.dt}/result.json",
            True)
