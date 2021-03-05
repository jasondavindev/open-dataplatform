#!/bin/bash

for file in $AIRFLOW_HOME/bootstrap/*.sh; do
  bash "$file" -H
done

exec "${@}"
