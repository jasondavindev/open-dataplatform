import argparse
from pyspark.sql import SparkSession


def check_table_exists(spark_session, database, table):
    return spark_session._jsparkSession.catalog().tableExists(database, table)


def save_table(spark, df, database, table, path, partitions=[]):
    if check_table_exists(spark, database, table):
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


parser = argparse.ArgumentParser(description="study case transform")
parser.add_argument('--db', required=True)
parser.add_argument('--table', required=True)
parser.add_argument('--date', required=True)
parser.add_argument('--hdfs-uri', required=True)
args = parser.parse_args()

HDFS_URI = args.hdfs_uri
DATALAKE_TRUSTED_LAYER_PATH = '/user/hive/warehouse/trusted/'

date = args.date
db = args.db
table = args.table

spark = SparkSession \
    .builder \
    .appName("study case transform") \
    .enableHiveSupport() \
    .getOrCreate()

query = """
SELECT
    event_name, count(*) as count, date
FROM
    study_case.insights
WHERE
    date = '%s'
GROUP BY
    1, 3
ORDER BY 2 DESC
""" % date

df = spark.sql(query)
df = df \
    .repartition('date') \
    .write \
    .mode('overwrite')

path = f"{HDFS_URI}{DATALAKE_TRUSTED_LAYER_PATH}{db}/{table}"

save_table(spark, df, db, table, path, ['date'])

spark.stop()
