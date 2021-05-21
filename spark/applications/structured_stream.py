from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import count, expr, col, struct, to_json, window, avg
from pyspark.sql.types import StringType

APPLICATION_TOPIC = 'example'

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
    .groupBy(window('value', '5 seconds', '5 seconds').alias('window'), 'favorite_color') \
    .agg(count('favorite_color').alias('count')) \
    .select(to_json(struct(['window', 'favorite_color', 'count'])).alias("value"))

query = output\
    .writeStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "broker:29092")\
    .option("topic", "output-topic")\
    .option("checkpointLocation", "/tmp/checkpoint")\
    .start()

query.awaitTermination()
