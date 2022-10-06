#!/bin/bash

THE_HOST=${HOST:="0.0.0.0"}
THE_PORT=${PORT:="5000"}

echo 'Start bp-beacon-python API Web Server'
exec gunicorn app:application --bind $THE_HOST:$THE_PORT --worker-class aiohttp.GunicornUVLoopWebWorker --workers 4