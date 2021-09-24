from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .getOrCreate()

data = [('random name', 1)]
columns = ['name', 'random_number']

df = spark.createDataFrame(data, columns)

df.show()