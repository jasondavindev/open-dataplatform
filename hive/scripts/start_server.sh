#!/bin/bash

hiveserver2 & until [ -f /tmp/hive/hive.log ];do sleep 1; echo Waiting log file;done
tail -f /tmp/hive/hive.log
