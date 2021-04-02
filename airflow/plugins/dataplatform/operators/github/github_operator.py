import logging

import requests
from json import dumps
from dataplatform.operators.json_to_hdfs_operator import JsonToHDFSOperator

log = logging.getLogger(__name__)


class GitHubToHDFSOperator(JsonToHDFSOperator):
    def __init__(
            self,
            profile,
            *args,
            **kwargs):
        self.profile = profile
        self.github_api = "https://api.github.com"
        self.github_headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        super().__init__(*args, **kwargs)

    def execute(self, context):
        response = requests.get(
            f"{self.github_api}/users/{self.profile}", headers=self.github_headers)
        json = response.json()

        self.put(path=f"/spark/{context['ds']}/{self.profile}.json",
                 data=dumps(json),
                 encoding='utf-8',
                 overwrite=True)
