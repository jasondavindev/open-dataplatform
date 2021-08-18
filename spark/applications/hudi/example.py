# Submit with: --conf "spark.serializer=org.apache.spark.serializer.KryoSerializer"

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("hive_example") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

data = [
    ('Java', 10, 1629244687223),
    ('Python', 15, 1629244787223),
    ('Scala', 5, 1629344687223)
]

basePath = "file:///tmp/hudi_tables"
columns = ['language', 'adopt', 'ts']
tableName = 'hudi_languages'


def show_table():
    spark.read.format('hudi').load(basePath + '/*').sort('adopt').show()


df = spark \
    .sparkContext \
    .parallelize(data) \
    .toDF(columns)

hudi_options = {
    'hoodie.table.name': tableName,
    'hoodie.datasource.write.recordkey.field': 'language',
    'hoodie.datasource.write.table.name': tableName,
    'hoodie.datasource.write.operation': 'upsert',
    'hoodie.datasource.write.precombine.field': 'ts',
    'hoodie.upsert.shuffle.parallelism': 2,
    'hoodie.insert.shuffle.parallelism': 2
}


df.write.format("hudi"). \
    options(**hudi_options). \
    mode("overwrite"). \
    save(basePath)


show_table()

# Test append
data = [
    ('Javascript', 20, 1629244687223),
    ('Ruby', 2, 1629244787223),
    ('Go', 15, 1629344687223)
]

ndf = spark.sparkContext.parallelize(data).toDF(columns)

ndf.write.format("hudi"). \
    options(**hudi_options). \
    mode("append"). \
    save(basePath)

show_table()

# Test update

data = [
    ('Java', 8, 1629244687223)
]

ndf = spark.sparkContext.parallelize(data).toDF(columns)

ndf.write.format("hudi"). \
    options(**hudi_options). \
    mode("append"). \
    save(basePath)

show_table()

# Test delete

data = [
    ('Java', 20, 1629244687223)
]

ndf = spark.sparkContext.parallelize(data).toDF(columns)

ndf.write.format("hudi"). \
    options(**hudi_options). \
    option('hoodie.datasource.write.operation', 'delete'). \
    mode("append"). \
    save(basePath)

show_table()
