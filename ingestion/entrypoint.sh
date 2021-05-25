#!/bin/bash
if [ ! -d "/app/node_modules" ]
then
    npm install
else
    echo "[OK] Modules"
fi

exec "$@"
