import json

from airflow.models.baseoperator import BaseOperator
from dataplatform.hooks.status_invest_hook import StatusInvestHook
from dataplatform.hooks.hdfs_hook import HDFSHook


class StocksToHDFSOperator(BaseOperator):
    def __init__(
            self,
            dt=None,
            status_invest_conn_id='status_invest_conn',
            hdfs_conn_id='hdfs_http',
            *args,
            **kwargs):
        self.status_invest_client = StatusInvestHook(
            conn_id=status_invest_conn_id)
        self.hdfs_hook = HDFSHook(hdfs_conn_id, 'airflow')
        self.dt = dt

        super().__init__(*args, **kwargs)

    def execute(self, context):
        stocks = self.status_invest_client.get_all_stocks()
        return self.hdfs_hook.put(
            path=f"/airflow/status_invest/dt={self.dt}/result.json",
            data=json.dumps(stocks),
            overwrite=True)
