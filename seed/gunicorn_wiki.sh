#!/bin/bash

NAME="sub_domain_wiki"
DJANGODIR=server_root/sub_domain/
SOCKFILE=server_root/run/gunicorn_sub_domain.sock
NUM_WORKERS=7
DJANGO_SETTINGS_MODULE=hello.settings
DJANGO_WSGI_MODULE=hello.wsgi

echo "Starting $NAME as `whoami`"

cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export LC_ALL='en_US.UTF-8'

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --log-level=debug \
  --bind=unix:$SOCKFILE


