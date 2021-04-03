import argparse
from pyspark.sql import SparkSession
import json

parser = argparse.ArgumentParser(description="Persist a JSON as Parquet")

parser.add_argument('--json-files-path', required=True)
parser.add_argument('--database', required=True)
parser.add_argument('--table', required=True)
parser.add_argument('--hdfs-uri', required=True)
args = parser.parse_args()

database = args.database
table = args.table
hdfs_uri = args.hdfs_uri

spark = SparkSession \
    .builder \
    .appName("Json to Parquet script") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")

df = spark \
    .read \
    .json(args.json_files_path)

df \
    .write \
    .mode('overwrite') \
    .saveAsTable(
        f"{database}.{table}",
        path=f"{hdfs_uri}/user/hive/warehouse/{database}/{table}",
        overwrite=True)

spark.stop()
