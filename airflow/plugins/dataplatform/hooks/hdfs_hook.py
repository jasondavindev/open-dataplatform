from airflow.hooks.base_hook import BaseHook
from hdfs import InsecureClient


class HDFSHook(BaseHook):
    def __init__(self, conn_id, user, *args, **kwargs):
        self.conn_id = conn_id
        self.user = user

        conn = self.get_connection(conn_id)
        conn_uri = conn.get_uri()
        self.client = InsecureClient(conn_uri, user=user)

    def __get_client(self):
        return self.client

    def put(
            self,
            path='',
            data={},
            overwrite=True,
            encoding='utf-8'):
        return self.__get_client().write(
            hdfs_path=path,
            data=data,
            overwrite=overwrite,
            encoding=encoding)
