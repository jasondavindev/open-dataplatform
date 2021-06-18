import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit


def check_table_exists(spark_session):
    return spark_session._jsparkSession.catalog().tableExists(database, table)


parser = argparse.ArgumentParser(description="Persist a JSON as Parquet")

parser.add_argument('--json-files-path', required=True)
parser.add_argument('--database', required=True)
parser.add_argument('--table', required=True)
parser.add_argument('--hdfs-uri', required=True)
parser.add_argument('--date', required=False)
parser.add_argument('--partitions', required=True)
args = parser.parse_args()

database = args.database
table = args.table
hdfs_uri = args.hdfs_uri
path = f"{hdfs_uri}/user/hive/warehouse/trusted/{database}/{table}"
partition_date = args.date
partitions = args.partitions.split(',')

spark = SparkSession \
    .builder \
    .appName("Json to Parquet script") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")

df = spark \
    .read \
    .json(args.json_files_path)

if partition_date:
    df = df.withColumn('date', lit(partition_date))

df = df \
    .repartition(*partitions) \
    .write \
    .mode('overwrite')

if check_table_exists(spark):
    print(f"Inserting into {database}.{table} on path={path}")
    df.insertInto(f"{database}.{table}", overwrite=False)
else:
    print(f"Saving table {database}.{table} on path={path}")
    df \
        .partitionBy(partitions) \
        .saveAsTable(
            f"{database}.{table}",
            path=path,
            overwrite=True)

spark.stop()
