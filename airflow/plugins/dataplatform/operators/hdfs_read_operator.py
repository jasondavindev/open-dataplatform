from airflow.models import BaseOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator


class HDFSReadOperator(BaseOperator):
    def __init__(
        self,
        file,
        *args,
        **kwargs
    ):
        self.file = file

    # def execute(self, context):
