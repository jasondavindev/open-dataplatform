import argparse
import json
from datetime import date
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

parser = argparse.ArgumentParser(description="Persist a JSON as Parquet")

parser.add_argument('--json-files-path', required=True)
parser.add_argument('--database', required=True)
parser.add_argument('--table', required=True)
parser.add_argument('--hdfs-uri', required=True)
args = parser.parse_args()

database = args.database
table = args.table
hdfs_uri = args.hdfs_uri
today = str(date.today())

spark = SparkSession \
    .builder \
    .appName("Json to Parquet script") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")

df = spark \
    .read \
    .json(args.json_files_path)

df = df.withColumn('date', lit(today))

df \
    .repartition('date') \
    .write \
    .mode('overwrite') \
    .partitionBy(['date']) \
    .saveAsTable(
        f"{database}.{table}",
        path=f"{hdfs_uri}/user/hive/warehouse/{database}/{table}",
        overwrite=True)

spark.stop()
