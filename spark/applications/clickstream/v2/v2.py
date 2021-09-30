import os
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import from_json
from pyspark.sql.types import *
from pyspark.sql.functions import col


def insert_into_table(df: DataFrame, _: int):
    df.write.insertInto('dumping.clickstream_v2', False)


schema = StructType([StructField('name', StringType()),
                    StructField('age', IntegerType())])

KAFKA_BROKER = os.getenv('KAFKA_BROKER')
APP_TOPIC = os.getenv('APP_TOPIC')

spark = SparkSession \
    .builder \
    .appName("clickstream_v2") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql('CREATE DATABASE IF NOT EXISTS dumping')
spark.sql("""
  CREATE TABLE IF NOT EXISTS dumping.clickstream_v2 (
    name STRING,
    age INT
  )
  STORED AS parquet
  """)

df = spark \
    .readStream \
    .format("kafka") \
    .option("failOnDataLoss", "false") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", APP_TOPIC) \
    .load()

df = df \
    .select(from_json(col('value').cast('string'), schema).alias('value')) \
    .select('value.name', 'value.age')

writer = df \
    .writeStream \
    .outputMode('append') \
    .format('parquet') \
    .option('checkpoint', '/tmp/checkpoint') \
    .foreachBatch(insert_into_table) \
    .start() \
    .awaitTermination()
