import argparse
from pyspark.sql import SparkSession
from datetime import date
from pyspark.sql.functions import lit, col

today = str(date.today())
parser = argparse.ArgumentParser(description="Filter best stocks")

parser.add_argument('--from-database', required=True)
parser.add_argument('--from-table', required=True)
parser.add_argument('--to-database', required=True)
parser.add_argument('--to-table', required=True)
parser.add_argument('--hdfs-uri', required=True)
args = parser.parse_args()

from_database = args.from_database
from_table = args.from_table
to_database = args.to_database
to_table = args.to_table
hdfs_uri = args.hdfs_uri

spark = SparkSession \
    .builder \
    .appName("best-stocks") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql(f"CREATE DATABASE IF NOT EXISTS {to_database}")

df = spark.table(f"{from_database}.{from_table}") \
    .select(
        col('companyname').alias('nome'),
        col('ticker'),
        col('p_l').alias('pl'),
        col('dy').alias('dividendo'),
        col('p_vp').alias('pvp'),
        col('lucros_cagr5'),
        col('dividaliquidapatrimonioliquido').alias('div_pat_liq'),
        col('dividaliquidaebit').alias('div_liq_ebit'),
        col('margembruta').alias('marg_bruta'),
        col('margemliquida').alias('marg_liq'),
        col('margemebit').alias('marg_ebit'),
        col('roe'),
        col('roic'),
        col('price').alias('preco'),
) \
    .filter(col('dy') >= 5) \
    .filter(col('dividaliquidapatrimonioliquido') < 3) \
    .filter(col('p_l') < 20) \
    .filter(col('lucros_cagr5') >= 5) \
    .filter(col('liquidezmediadiaria') > 1000000) \
    .orderBy(
        col('dy').desc(),
        col('pl').asc(),
        col('dividaliquidaebit').asc(),
        col('margemliquida').desc(),
        col('lucros_cagr5').desc()) \
    .withColumn('date', lit(today))

df \
    .repartition('date') \
    .write \
    .mode('overwrite') \
    .partitionBy(['date']) \
    .saveAsTable(
        f"{to_database}.{to_table}",
        path=f"{hdfs_uri}/user/hive/warehouse/{to_database}/{to_table}",
        overwrite=True)

spark.stop()
