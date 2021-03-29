# HDFS

This module creates the Distributed File System (Hadoop v3.3.0) with no permissions folder. To access the HDFS points to `namenode:8020` hostname.

## How to run

Start up the containers

```bash
docker-compose up
```

**The namenode hostname is replaced in runtime by entrypoint script.**

## Scripts

In the Makefile, is provided `hdfs dfs` commands (ls, mkdir, chown, cat, rm and copyFromLocal).
