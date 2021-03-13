from pyspark.sql import SparkSession

database = 'spark_test'
table = 'users'

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL Hive integration example") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")

columns = ['id', 'name', 'dt']
values = [
    (1, 'jason', '2021-03-12'),
    (2, 'davin', '2021-03-11'),
]

df = spark.createDataFrame(values, columns)

df.show()

df \
    .repartition('dt') \
    .write \
    .mode('overwrite') \
    .partitionBy(['dt']) \
    .saveAsTable(
        f"{database}.{table}",
        path=f"hdfs://namenode:8020/user/hive/warehouse/{database}/{table}",
        overwrite=True)

spark.stop()
