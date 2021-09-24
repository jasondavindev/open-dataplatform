from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .getOrCreate()

data = [('jason', 1)]
columns = ['name', 'random_number']

df = spark.createDataFrame(data, columns)

df.show()