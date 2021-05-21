from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import count, expr, col, to_json, window, avg
from pyspark.sql.types import StringType

APPLICATION_TOPIC = 'example-2'

jsonFormatSchema = """
{
  "type": "record",
  "name": "Example",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "favorite_color", "type": "string"},
    {"name": "event_time", "type": "long"}
  ]
}
"""

spark = SparkSession \
    .builder \
    .appName("stream-test") \
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
    .select(col('parsedValue.event_time').cast('timestamp').alias('value'), 'parsedValue.name', 'parsedValue.favorite_color') \
    .withWatermark('value', '5 seconds') \
    .groupBy(window('value', '5 seconds', '5 seconds'), 'favorite_color') \
    .agg(count('*').alias('count'))

query = output \
    .writeStream \
    .outputMode('complete') \
    .option('truncate', False) \
    .format('console') \
    .start()

# query = output\
#     .writeStream\
#     .format("kafka")\
#     .option("kafka.bootstrap.servers", "broker:29092")\
#     .option("topic", "output-topic")\
#     .option("checkpointLocation", "/tmp/checkpoint")\
#     .start()

query.awaitTermination()
