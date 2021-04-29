from airflow.hooks.http_hook import HttpHook
from urllib.parse import urlencode


class StatusInvestHook(HttpHook):
    def __init__(
        self,
        conn_id="status_invest_conn",
    ):
        self.conn_id = conn_id
        super().__init__(method='GET', http_conn_id=conn_id)

    def __get(self, endpoint='', query=None, headers={}):
        return self.run(endpoint=endpoint, data=query, headers=headers).json()

    def get_all_stocks(self):
        params = urlencode({'CategoryType': 1, 'search': {}})
        headers = {'User-Agent': 'PostmanRuntime/7.26.10'}
        return self.__get(
            endpoint='/category/advancedsearchresult',
            query=params,
            headers=headers)
