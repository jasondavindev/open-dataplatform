import logging

from airflow.models import BaseOperator
import requests
from json import dumps
from dataplatform.hooks.hdfs_hook import HDFSHook

log = logging.getLogger(__name__)


class GitHubToHDFSOperator(BaseOperator):
    def __init__(
            self,
            profile,
            conn_id,
            *args,
            **kwargs):
        self.profile = profile
        self.github_api = "https://api.github.com"
        self.conn_id = conn_id
        self.github_headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        self.client = HDFSHook("hdfs_http", "airflow").get_client()
        super().__init__(*args, **kwargs)

    def execute(self, context):
        response = requests.get(
            f"{self.github_api}/users/{self.profile}", headers=self.github_headers)
        json = response.json()

        self.client.write(f"/spark/{context['ds']}/{self.profile}.json",
                          data=dumps(json),
                          encoding='utf-8',
                          overwrite=True)
