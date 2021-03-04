'''
You should create the spark folder in HDFS. Use
makefile commands to create by running:
make mkdir dir=/spark
make chown user=spark dir=/spark
'''

from pyspark.sql import SparkSession

HDFS_URL = 'hdfs://namenode:8020'

sparkSession = SparkSession.builder.appName(
    "example-pyspark-read-and-write").getOrCreate()


def write():
    data = [('First', 1), ('Second', 2), ('Third', 3),
            ('Fourth', 4), ('Fifth', 5)]

    df = sparkSession.createDataFrame(data)
    df.write.mode('overwrite').csv(f"{HDFS_URL}/spark/files")


def read():
    df_load = sparkSession.read.csv(f"{HDFS_URL}/spark/files")
    df_load.show()

write()
read()
