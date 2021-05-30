import argparse
from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro, to_avro
from pyspark.sql.functions import count, expr, col, lit, struct, to_json, to_timestamp, window

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
  "type": "string",
  "name": "a6-key"
}
"""

spark = SparkSession \
    .builder \
    .appName("clickstream") \
    .config('spark.sql.streaming.stateStore.stateSchemaCheck', False) \
    .getOrCreate()

df = spark \
    .readStream\
    .format("kafka")\
    .option("failOnDataLoss", "false")\
    .option("kafka.bootstrap.servers", "broker:29092")\
    .option("subscribe", APPLICATION_TOPIC)\
    .load()

output = df \
    .withColumn('fixedValue', expr("substring(value, 6, length(value)-5)")) \
    .withColumn('fixedKey', expr('cast(unbase64(substring(key, 6, length(key)-5)) as string)')) \
    .select('topic', 'fixedValue', 'fixedKey') \
    .withColumn('parsedValue', from_avro('fixedValue', input_event_schema,  {"mode": "FAILFAST"})) \
    .withColumn('event_time', to_timestamp(col('parsedValue.event_time'))) \
    .withColumn('username', col('parsedValue.username')) \
    .withColumn('page', col('parsedValue.page')) \
    .withColumn('event_name', col('parsedValue.event_name')) \
    .select('event_time', 'event_name', 'username', 'page', 'fixedKey') \
    .select(
      to_avro(struct(['event_time', 'username', 'page', 'event_name']), input_event_schema).alias('value'),
      to_avro(col('fixedKey'), output_event_schema).alias('key'))
      # .select(to_avro(struct(['start_date', 'start_time', 'username', 'page', 'event_name', 'count'])).alias("value"))

query = output\
    .writeStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "broker:29092")\
    .option("topic", output_topic)\
    .option("checkpointLocation", "/tmp/checkpoint")\
    .start()

query.awaitTermination()
