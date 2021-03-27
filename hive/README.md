# What is

Hive module is the module contain

- Apache Hive as a data warehouse
- Hive metastore to store metadata of tables and databases
- Hue for friendly user interface to manage hive

# How to run

Creates the necessary folders on HDFS

```bash
sh scripts/create_folders.sh
```

And start docker containers

```bash
docker-compose up
```

**Obs**: if you need only hive metastore, then starts with `docker-compose up hive-metastore`. For the Kafka connector and Trino read the entities of Hive, only the Hive metastore is necessary.
