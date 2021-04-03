from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.hooks.base_hook import BaseHook


class JsonToParquetOperator(SparkSubmitOperator):
    template_fields = ['_application_args']

    def __init__(
        self,
        json_files_path='',
        hive_database='',
        hive_table='',
        hdfs_conn_id='hdfs',
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._spark_binary = 'spark-submit'
        self._json_files_path = json_files_path
        self._hive_database = hive_database
        self._hive_table = hive_table
        self._hdfs_conn_id = hdfs_conn_id
        self._application = f"{self.hdfs_conn}/spark/scripts/json_to_parquet.py"

    def application_args(self, context):
        _application_args = [
            '--json-files-path', self.hdfs_conn + self._json_files_path,
            '--database', self._hive_database,
            '--table', self._hive_table,
            '--hdfs-uri', self.hdfs_conn
        ]

        self._application_args = _application_args

        return _application_args

    def execute(self, context):
        if self.application_args(context) is not None:
            super().execute(context)

    @property
    def hdfs_conn(self):
        conn = BaseHook.get_connection(self._hdfs_conn_id)
        return f"hdfs://{conn.host}:{conn.port}"
