from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import expr, col, to_json
from pyspark.sql.types import StringType

jsonFormatSchema = """
{
  "type": "record",
  "name": "Example",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "favorite_color", "type": "string"}
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
    .option("subscribe", "topic-example")\
    .load()

output = df \
    .withColumn('key', col("key").cast(StringType())) \
    .withColumn('fixedValue', expr("substring(value, 6, length(value)-5)")) \
    .select('topic', 'partition', 'offset', 'timestamp', 'timestampType', 'key', 'fixedValue') \
    .withColumn('parsedValue', from_avro('fixedValue', jsonFormatSchema,  {"mode": "FAILFAST"})) \
    .withColumn('value', to_json('parsedValue'))


query = output\
    .writeStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "broker:29092")\
    .option("topic", "output-topic")\
    .option("checkpointLocation", "/tmp/checkpoint")\
    .start()

query.awaitTermination()
