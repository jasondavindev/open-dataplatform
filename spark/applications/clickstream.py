import argparse
from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import count, expr, col, struct, to_json, to_timestamp, window

parser = argparse.ArgumentParser(
    description='Arguments for clickstream application')
parser.add_argument('--topic', default='clickstream')
parser.add_argument('--event-window', default='5 seconds')
parser.add_argument('--watermark', default='5 seconds')
parser.add_argument('--output-topic', required=True)
args = parser.parse_args()

APPLICATION_TOPIC = args.topic
event_window_time = args.event_window
watermark_time = args.watermark
output_topic = args.output_topic

input_event_schema = """
{
  "type": "record",
  "name": "input_event",
  "fields": [
    {"name": "username", "type": "string"},
    {"name": "page", "type": "string"},
    {"name": "event_name", "type": "string"},
    {"name": "event_time", "type": "long"}
  ]
}
"""

output_event_schema = """
{
  "type": "record",
  "name": "output_event",
  "fields": [
    {"name": "start_date", "type": "string"},
    {"name": "start_time", "type": "string"},
    {"name": "username", "type": "string"},
    {"name": "page", "type": "string"},
    {"name": "event_name", "type": "string"},
    {"name": "count", "type": "long"}
  ]
}
"""

spark = SparkSession \
    .builder \
    .appName("clickstream") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("""
  create table if not exists dumping.testando (
    start_date string,
    start_time string,
    username string,
    page string, count int
  )
  partitioned by (event_name string)
  stored as parquet
  location '/user/hive/warehouse/dumping/testando'
  """)

df = spark \
    .readStream\
    .format("kafka")\
    .option("failOnDataLoss", "false")\
    .option("kafka.bootstrap.servers", "broker:29092")\
    .option("subscribe", APPLICATION_TOPIC)\
    .load()

output = df \
    .withColumn('fixedValue', expr("substring(value, 6, length(value)-5)")) \
    .select('topic', 'fixedValue') \
    .withColumn('parsedValue', from_avro('fixedValue', input_event_schema,  {"mode": "FAILFAST"})) \
    .withColumn('event_time', to_timestamp(col('parsedValue.event_time'))) \
    .withColumn('username', col('parsedValue.username')) \
    .withColumn('page', col('parsedValue.page')) \
    .withColumn('event_name', col('parsedValue.event_name')) \
    .select('event_time', 'event_name', 'username', 'page') \
    .withWatermark('event_time', watermark_time) \
    .groupBy(window('event_time', event_window_time), 'event_name', 'page', 'username') \
    .agg(count('window').alias('count')) \
    .withColumn('start_date', expr("substring(window.start, 0, 10)")) \
    .withColumn('start_time', expr("substring(window.start, 12, 8)")) \
    .select('start_date', 'start_time', 'username', 'page', 'event_name', 'count') \
    .repartition('event_name')

query = output\
    .writeStream\
    .outputMode('append') \
    .format('parquet') \
    .option('path', '/user/hive/warehouse/dumping/testando') \
    .option("checkpointLocation", "/tmp/checkpoint")\
    .partitionBy(['event_name']) \
    .start()

query.awaitTermination()
