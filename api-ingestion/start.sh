#!/bin/bash

sudo kill $(lsof -t -i :${PORT:-7777}) || true
go run server/main.go
