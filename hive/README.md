# Hive and Hive metastore

The Hive metastore is used to store the metadata (e.g. table schema and partitions). The data stored by Kafka connector and Spark scripts are in Parquet format.

## What is

Hive module is the module contain

- Apache Hive as a data warehouse
- Hive metastore to store metadata of tables and databases
- Hue for friendly user interface to manage hive

## How to run

Start up the containers

```bash
docker-compose up
```

**Obs**: For the project workflow, starts only the hive metastore container. The Hive it is a data warehouse component and not is necessary. To query the data, Trino is used.
