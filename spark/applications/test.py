from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import window

# `from_avro` requires Avro schema in JSON string format.
jsonFormatSchema = """
{
  "type": "record",
  "name": "Example",
  "fields": [
    {"name": "key", "type": "string"},
    {"name": "value", "type": "string"}
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
    .option("subscribe", "topic-abc")\
    .load()

output = df \
    .select(
        from_avro("value", jsonFormatSchema).alias("teste")) \
    .select("teste.value").alias("timestamp")
    # .groupBy(window("timestamp", "5 seconds"))


query = output\
    .writeStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "broker:29092")\
    .option("topic", "output-topic")\
    .option("checkpointLocation", "/tmp/checkpoint")\
    .start()

query.awaitTermination()
