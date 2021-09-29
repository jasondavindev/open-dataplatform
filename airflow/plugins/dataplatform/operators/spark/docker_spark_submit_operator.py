import ntpath
import os
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.hooks.webhdfs_hook import WebHDFSHook
from airflow.hooks.base_hook import BaseHook


class DockerSparkSubmitOperator(SparkSubmitOperator):
    def __init__(self,
                 hdfs_http_conn_id='hdfs_http',
                 hdfs_conn_id='hdfs',
                 conn_id='spark',
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._deploy_mode = os.getenv('SPARK_DEPLOY_MODE')
        self.define_connection(conn_id)
        self._hdfs_hook = WebHDFSHook(hdfs_http_conn_id)
        self._hdfs_http_conn_id = hdfs_http_conn_id
        self._hdfs_conn_id = hdfs_conn_id
        self._old_application = kwargs['application']
        self._application = self._get_application()

    @property
    def _hdfs_conn_string(self):
        conn = BaseHook().get_connection(self._hdfs_conn_id)
        return f"hdfs://{conn.host}:{conn.port}"

    @property
    def _new_application_path(self):
        basename = ntpath.basename(self._old_application)
        return f"/spark/scripts/{basename}"

    def _get_application(self):
        return f"{self._hdfs_conn_string}/{self._new_application_path}"

    def load_script(self):
        path_prefix = os.getenv("SCRIPTS_PATH_PREFIX") or ""
        print(f"Uploading file {path_prefix}{self._old_application}")

        self._hdfs_hook.load_file(
            f"{path_prefix}{self._old_application}",
            self._new_application_path,
            overwrite=True)

    def define_default_confs(self):
        if self._deploy_mode != 'cluster':
            return self._conf

        self._conf = {
            **(self._conf or {}),
            **{
                'spark.kubernetes.container.image': os.getenv('SPARK_IMAGE'),
                'spark.kubernetes.authenticate.driver.serviceAccountName': 'spark',
                'spark.kubernetes.namespace': 'dataplatform',
                'spark.hadoop.hive.metastore.uris': os.getenv('METASTORE_URI')
            }}

        return self._conf

    def define_connection(self, conn):
        self._conn_id = 'spark-cluster' if self._deploy_mode == 'cluster' else conn

    def execute(self, context):
        self.define_default_confs()
        self.load_script()
        super().execute(context)
