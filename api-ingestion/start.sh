#!/bin/bash

PID=$(lsof -t -i :${PORT:-7777})
if [ -n "$PID" ];then kill $PID;fi
go run server/main.go
