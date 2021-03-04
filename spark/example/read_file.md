# Read file

Connect to hadoop container, create file and move to hdfs

```bash
docker exec -ti namenode bash
# inside container
for i in {1..1000}; do echo "Line $i" >> /tmp/file; done
hdfs dfs -copyFromLocal -f /tmp/file /tmp/file
```

Connect to spark container and run

```bash
spark-shell --master spark://spark-master:7077
```

In scala shell run

```scala
var file = sc.textFile("hdfs://namenode:8020/tmp/file")

println("##Get data Using collect")

file.collect().foreach(f=>{
    println(f)
})
```
