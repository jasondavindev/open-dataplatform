import argparse
from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import count, expr, col, struct, to_json, window

parser = argparse.ArgumentParser(description='Arguments for clickstream application')
parser.add_argument('--topic', default='clickstream')
args = parser.parse_args()

APPLICATION_TOPIC = args.topic

jsonFormatSchema = """
{
  "type": "record",
  "name": "user_event",
  "fields": [
    {"name": "username", "type": "string"},
    {"name": "page", "type": "string"},
    {"name": "event_name", "type": "string"},
    {"name": "event_time", "type": "long"}
  ]
}
"""

spark = SparkSession \
    .builder \
    .appName("clickstream") \
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
    .select('topic', 'fixedValue') \
    .withColumn('parsedValue', from_avro('fixedValue', jsonFormatSchema,  {"mode": "FAILFAST"})) \
    .withColumn('event_time', col('parsedValue.event_time').cast('timestamp')) \
    .withColumn('username', col('parsedValue.username')) \
    .withColumn('page', col('parsedValue.page')) \
    .withColumn('event_name', col('parsedValue.event_name')) \
    .select('event_time', 'event_name', 'username', 'page') \
    .withWatermark('event_time', '5 seconds') \
    .groupBy(window('event_time', '5 seconds'), 'event_name', 'page', 'username') \
    .agg(count('window').alias('count')) \
    .select(to_json(struct(['window', 'username', 'page', 'event_name', 'count'])).alias("value"))

query = output\
    .writeStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "broker:29092")\
    .option("topic", "output-topic")\
    .option("checkpointLocation", "/tmp/checkpoint")\
    .start()

query.awaitTermination()
