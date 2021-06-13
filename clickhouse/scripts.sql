CREATE TABLE queue (
    timestamp UInt64,
    level String,
    message String
) ENGINE = Kafka(
    'broker:29092',
    'topic-example',
    'group1',
    'JSONEachRow'
);

CREATE TABLE daily (
    day DateTime,
    level String,
    total UInt64
) ENGINE = MergeTree PARTITION BY toYYYYMM(day)
ORDER BY
    (day);

CREATE MATERIALIZED VIEW consumer TO daily AS
SELECT
    toDateTime(timestamp) AS day,
    level,
    count() as total
FROM
    queue
GROUP BY
    day,
    level;

SELECT
    level,
    sum(total)
FROM
    daily
GROUP BY
    level;