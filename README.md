# Open Data Platform

## Problema

- Grande volume de dados
- Custos

## Motivação

- Aumento do fluxo e troca de informações
- Grande volume de dados
- Decisões de negócio
- Experiência personalizada para cada usuário
- Problemas de arquitetura no mundo de hoje
- Análise de informações em tempo real
- Plataformas de dados
- Tecnologias modernas
- Custos de plataformas robustas
- Soluções open-source

## Solução

Criar uma plataforma de dados com tecnologias preferencialmente open-source. Objetivo final é criar uma plataforma de dados capaz de suportar uma quantidade massiva de dados e ferramental para análises em tempo real e histórica.

## Arquitetura

![Initial archtecture](./doc/images/architecture.jpeg)

## Tecnologias

### Apache Spark

Ferramenta para processamento de dados em batch e stream.

### Apache Airflow

Ferramenta para gerenciamento de tarefas ETL usando DAGs (Direct Acyclic Graph).

### Apache Kafka

Ferramenta message broker para transmissão de eventos/mensagens de modo distribuído.

### Apache Parquet

Formato colunar de armazenamento de dados.

### HDFS

Sistema de arquivos distribuído do eco sistema Hadoop.


### Apache Trino (ou PrestoDB)

Ferramenta Query Engina - para operações DML em bases não SQL.

### Apache Hive Metastore

Ferramenta para armazenamento de metadados de arquivos no HDFS. Para armazenamento do schema, partições etc.
