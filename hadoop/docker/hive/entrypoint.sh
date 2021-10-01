#!/bin/bash
if [ ! -f populated -a "$NODE_TYPE" == "metastore" ]; then
    schematool -dbType postgres -initSchema
    touch populated
fi

exec "$@"
