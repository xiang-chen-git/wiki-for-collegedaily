#!/bin/bash
# new_school.sh
# Dong Jiaqing
# 2013.12.21
SUPERVISOR_CONF_DIR=/etc/supervisor/conf.d/
NGINX_CONF_DIR=/etc/nginx/sites-enabled/

USAGE="Usage: `basename $0` sub_domain"
[ $# -lt 1 ] && {
    echo $USAGE
    exit 1
}
SUB_DOMAIN=$1

SUPERVISOR_CONF=$SUPERVISOR_CONF_DIR/$SUB_DOMAIN.conf
NGINX_CONF=$NGINX_CONF_DIR/$SUB_DOMAIN.nginx
[ -e $SUPERVISOR_CONF ] && rm $SUPERVISOR_CONF
[ -e $NGINX_CONF ] && rm $NGINX_CONF

supervisorctl reread
supervisorctl update
nginx -s reload
