import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

DATALAKE_TRUSTED_LAYER_PATH = '/user/hive/warehouse/trusted/'


def spark_session():
    return SparkSession \
        .builder \
        .appName("Json to Parquet script") \
        .enableHiveSupport() \
        .getOrCreate()


def get_app_arguments():
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
    partition_date = args.date
    partitions = args.partitions.split(',')
    json_files_path = args.json_files_path

    return [database, table, hdfs_uri, partition_date, partitions, json_files_path]


def check_table_exists(spark_session):
    return spark_session._jsparkSession.catalog().tableExists(database, table)


def create_database_if_not_exist(spark, database):
    return spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")


def read_json_file(spark, path):
    return spark \
        .read \
        .json(path)


def get_writer(df, partition_date=None, partitions=[]):
    if partition_date:
        df = df.withColumn('date', lit(partition_date))

    return df \
        .repartition(*partitions) \
        .write \
        .mode('overwrite')


def save_table(spark, df, database, table, path, partitions=[]):
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


[database, table, hdfs_uri, partition_date,
    partitions, json_files_path] = get_app_arguments()
path = f"{hdfs_uri}{DATALAKE_TRUSTED_LAYER_PATH}{database}/{table}"

spark = spark_session()
create_database_if_not_exist(spark, database)

df = read_json_file(spark, json_files_path)
df = get_writer(df, partition_date, partitions)
save_table(spark, df, database, table, path, partitions)

spark.stop()
