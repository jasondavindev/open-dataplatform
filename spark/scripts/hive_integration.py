from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL Hive integration example") \
    .enableHiveSupport() \
    .getOrCreate()

hdfs_uri = 'hdfs://namenode:8020'
database = 'spark_warehouse'
hive_warehouse = '/user/hive/warehouse/'
database_location = f"{hdfs_uri}{hive_warehouse}{database}"
table = 'users'

spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")

columns = ['name', 'country', 'dt']
values = [
    ('jason', 'brazil', '2021-03-12'),
    ('juca', 'italy', '2021-03-12'),
    ('juju', 'brazil', '2021-03-11'),
    ('jubileu', 'germany', '2021-03-10')
]

df = spark.createDataFrame(values, columns)

df.show()

df.repartition('dt') \
    .write \
    .mode('overwrite') \
    .partitionBy(['dt']) \
    .saveAsTable(f"{database}.{table}", path=database_location)
