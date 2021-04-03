from airflow.models import BaseOperator
from dataplatform.hooks.hdfs_hook import HDFSHook


class JsonToHDFSOperator(BaseOperator):
    def __init__(self, conn_id='hdfs_conn', *args, **kwargs):
        self.conn_id = conn_id
        self.__hdfs_hook = HDFSHook(conn_id=conn_id, user='airflow')
        super().__init__(*args, **kwargs)

    def put(self, **args):
        self.__hdfs_hook.put(**args)
