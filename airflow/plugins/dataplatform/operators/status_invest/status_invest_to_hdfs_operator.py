import json

from airflow.models.baseoperator import BaseOperator
from dataplatform.hooks.status_invest_hook import StatusInvestHook
from dataplatform.hooks.hdfs_hook import HDFSHook


class StatusInvestToHDFSOperator(BaseOperator):
    template_fields = ['dt']

    def __init__(
            self,
            dt=None,
            status_invest_conn_id='status_invest_conn',
            hdfs_conn_id='hdfs_http',
            category_type='stocks',
            *args,
            **kwargs):
        self.status_invest_client = StatusInvestHook(
            conn_id=status_invest_conn_id)
        self.hdfs_hook = HDFSHook(hdfs_conn_id, 'airflow')
        self.dt = dt
        self.category_type = category_type
        self.define_map_category_type()

        super().__init__(*args, **kwargs)

    def define_map_category_type(self):
        self.category_types = {
            'stocks': self.status_invest_client.get_all_stocks,
            'fiis': self.status_invest_client.get_all_fiis
        }

    def execute(self, context):
        data = self.category_types[self.category_type]()
        return self.hdfs_hook.put(
            path=f"/user/hive/warehouse/raw/status_invest/{self.category_type}/dt={self.dt}/result.json",
            data=json.dumps(data),
            overwrite=True)
