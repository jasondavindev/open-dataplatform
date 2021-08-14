from airflow.hooks.base import BaseHook


def get_hdfs_http_url():
    hook = BaseHook().get_connection('hdfs_http')
    return f"http://{hook.host}:{hook.port}"


def get_hdfs_rpc_uri():
    hook = BaseHook().get_connection('hdfs')
    return f"hdfs://{hook.host}:{hook.port}"
