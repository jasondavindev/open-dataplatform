#!/bin/bash

function bootstrap {
  for file in $AIRFLOW_HOME/bootstrap/*.sh; do
    bash "$file" -H
  done
}

case "$1" in
  webserver)
    bootstrap
    sleep 2
    exec airflow "$@"
    ;;
  scheduler)
    exec airflow "$@"
    ;;
  *)
    exec "$@"
    ;;
esac
