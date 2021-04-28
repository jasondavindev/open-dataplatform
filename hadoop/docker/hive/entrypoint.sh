#!/bin/bash
if [ ! -f populated ]; then
    schematool -dbType postgres -initSchema
    touch populated
fi

exec "$@"
