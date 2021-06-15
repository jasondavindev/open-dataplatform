CREATE TABLE real_time (
    event_time UInt64,
    event_name String,
    username String,
    page String
) ENGINE = Kafka() SETTINGS kafka_broker_list = 'broker:29092',
kafka_topic_list = 'clickstream',
kafka_group_name = 'group_clickstream',
kafka_format = 'AvroConfluent',
format_avro_schema_registry_url = 'http://schema-registry:8081';

CREATE TABLE clickstream (
    event_time DateTime,
    event_name String,
    username String,
    page String
) ENGINE = MergeTree PARTITION BY toYYYYMM(event_time)
ORDER BY
    (event_time);

CREATE MATERIALIZED VIEW consumer_clickstream TO clickstream AS
SELECT
    toDateTime(event_time) AS event_time,
    event_name,
    username,
    page
FROM
    real_time;
