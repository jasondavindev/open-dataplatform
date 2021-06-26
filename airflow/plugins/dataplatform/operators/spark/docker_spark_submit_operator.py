import ntpath
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.hooks.webhdfs_hook import WebHDFSHook
from airflow.hooks.base_hook import BaseHook


class DockerSparkSubmitOperator(SparkSubmitOperator):
    def __init__(self,
                 hdfs_http_conn_id='hdfs_http',
                 hdfs_conn_id='hdfs',
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._hdfs_hook = WebHDFSHook(hdfs_http_conn_id)
        self._hdfs_http_conn_id = hdfs_http_conn_id
        self._hdfs_conn_id = hdfs_conn_id
        self._old_application = kwargs['application']
        self._application = self._get_application()
        self._conf = self._get_conf()

    @property
    def _hdfs_conn_string(self):
        conn = BaseHook().get_connection(self._hdfs_conn_id)
        return f"hdfs://{conn.host}:{conn.port}"

    @property
    def _new_application_path(self):
        basename = ntpath.basename(self._old_application)
        return f"/spark/scripts/{basename}"

    def _get_conf(self):
        return {
            'spark.sql.warehouse.dir': 'hdfs://namenode:8020/user/hive/warehouse',
        }

    def _get_application(self):
        return f"{self._hdfs_conn_string}/{self._new_application_path}"

    def load_script(self):
        self._hdfs_hook.load_file(
            self._old_application, self._new_application_path, overwrite=True)

    def execute(self, context):
        self.load_script()
        super().execute(context)
