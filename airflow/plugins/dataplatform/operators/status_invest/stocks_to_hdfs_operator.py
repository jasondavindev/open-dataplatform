import json

from dataplatform.operators.json_to_hdfs_operator import JsonToHDFSOperator
from dataplatform.hooks.status_invest_hook import StatusInvestHook


class StocksToHDFSOperator(JsonToHDFSOperator):
    def __init__(
            self,
            status_invest_conn_id='status_invest_conn',
            hdfs_conn_id='hdfs_http',
            *args,
            **kwargs):
        self.status_invest_client = StatusInvestHook(
            conn_id=status_invest_conn_id)
        super().__init__(conn_id=hdfs_conn_id, *args, **kwargs)

    def execute(self, context):
        ds = context['ds']
        stocks = self.status_invest_client.get_all_stocks()
        return self.put(
            path=f"/airflow/status_invest/dt={ds}/{ds}.json",
            data=json.dumps(stocks),
            overwrite=True)
