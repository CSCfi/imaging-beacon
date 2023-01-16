#!/bin/bash

THE_HOST=${APP_HOST:="0.0.0.0"}
THE_PORT=${APP_PORT:="8080"}

echo 'start imaging-beacon server'
exec gunicorn api.app:init --bind $THE_HOST:$THE_PORT --worker-class aiohttp.GunicornUVLoopWebWorker --workers 2
