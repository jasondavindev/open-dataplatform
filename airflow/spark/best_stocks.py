import argparse
from pyspark.sql import SparkSession

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

df = spark.sql("""
SELECT
    companyname AS nome, ticker, p_l AS pl, dy AS dividendo, p_vp AS pvp, lucros_cagr5, dividaliquidapatrimonioliquido AS div_pat_liq,
    dividaliquidaebit AS div_liq_ebit, margembruta AS marg_bruta, margemliquida AS marg_liq, roe, roic, price AS preco, date
FROM
    %s.%s
WHERE
    dy >= 5 AND
    dividaliquidapatrimonioliquido < 3 AND
    p_l < 20 AND
    lucros_cagr5 >= 5 AND
    liquidezmediadiaria > 1000000
ORDER BY
    dy DESC, pl, dividaliquidaebit, margemliquida DESC, lucros_cagr5 DESC
""" % (from_database, from_table))

df \
    .repartition('date') \
    .write \
    .mode('overwrite') \
    .partitionBy(['date']) \
    .saveAsTable(
        f"{to_database}.{to_table}",
        path=f"{hdfs_uri}/user/hive/warehouse/refined/{to_database}/{to_table}",
        overwrite=True)

spark.stop()
