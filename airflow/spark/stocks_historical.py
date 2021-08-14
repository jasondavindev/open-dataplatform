import argparse
import requests
from functools import reduce
from time import sleep
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from datetime import datetime, date


def get_stock_historical(ticker):
    return requests.post('https://statusinvest.com.br/acao/indicatorhistorical', {
        'ticker': ticker.upper(),
        'time': 5
    }).json()


parser = argparse.ArgumentParser()
parser.add_argument('--stocks-database', required=True)
parser.add_argument('--stocks-table', required=True)
parser.add_argument('--historical-database', required=True)
parser.add_argument('--historical-table', required=True)
parser.add_argument('--hdfs-uri', required=True)
args = parser.parse_args()

stocks_database = args.stocks_database
stocks_table = args.stocks_table
historical_database = args.historical_database
historical_table = args.historical_table
hdfs_uri = args.hdfs_uri

spark = SparkSession \
    .builder \
    .appName("stocks-historical") \
    .enableHiveSupport() \
    .getOrCreate()

tickers = spark.table(f"{stocks_database}.{stocks_table}") \
    .select('ticker') \
    .distinct() \
    .collect()

dfs = []

for row in tickers:
    ticker = row.ticker.upper()
    print(f"[STATUS INVEST] Search by ticker {ticker}")
    response = get_stock_historical(ticker)
    data = response['data']
    df = spark.createDataFrame(data) \
        .select('key', 'actual', 'avg', 'avgDifference') \
        .withColumn('ticker', lit(ticker))
    dfs.append(df)
    sleep(1)

dfs = reduce(lambda x, y: y.union(x), dfs)

dfs \
    .write \
    .mode('overwrite') \
    .saveAsTable(
        f"{historical_database}.{historical_table}",
        overwrite=True,
        path=f"{hdfs_uri}/user/hive/warehouse/refined/{historical_database}/{historical_table}")

spark.stop()
