import json
import requests

from airflow.models.baseoperator import BaseOperator
from dataplatform.hooks.hdfs_hook import HDFSHook


class StudyCaseOperator(BaseOperator):
    template_fields = ['dt']

    def __init__(
            self,
            dt=None,
            count=30,
            hdfs_conn_id='hdfs_http',
            *args,
            **kwargs):
        self.hdfs_hook = HDFSHook(hdfs_conn_id, 'airflow')
        self.dt = dt
        self.count = count
        self.ingestion_api_url = 'http://api:3000'

        super().__init__(*args, **kwargs)

    def _get_insights(self):
        return requests.get(f'{self.ingestion_api_url}/records', {
            'count': self.count,
            'date': self.dt
        }).json()

    def execute(self, context):
        data = self._get_insights()
        print(data)

        return self.hdfs_hook.put(
            path=f"/user/hive/warehouse/raw/study_case/insights/dt={self.dt}/result.json",
            data=json.dumps(data),
            overwrite=True)
