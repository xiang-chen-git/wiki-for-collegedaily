#!/bin/bash

NAME="admin_app"
DJANGODIR=/home/jiaqing/webapps/admin_campus/
SOCKFILE=/home/jiaqing/webapps/run/gunicorn_campus.sock
NUM_WORKERS=7
DJANGO_SETTINGS_MODULE=admin_campus.settings
DJANGO_WSGI_MODULE=admin_campus.wsgi

echo "Starting $NAME as `whoami`"

cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --log-level=debug \
  --bind=unix:$SOCKFILE


