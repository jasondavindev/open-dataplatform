#!/bin/bash
ENV=${ENV:-dev}

GOCMD="go run server/main.go"

if [ "$ENV" == "dev" ];then
    nodemon -e go --exec $GOCMD -w .
else
    echo "Starting server..."
    sh -c "$GOCMD"
fi
