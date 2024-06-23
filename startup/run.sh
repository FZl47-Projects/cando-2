#!/bin/bash

cd /root/projects/cando-2
source venv/bin/activate

nohup uwsgi --ini startup/uwsgi.ini > ./logs/server.log  &

nohup python src/manage.py qcluster > ./logs/qcluster.log &

nohup python src/manage.py init_task > ./logs/task.log &