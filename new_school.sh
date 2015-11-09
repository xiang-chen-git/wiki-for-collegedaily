#!/bin/bash
# new_school.sh
# Dong Jiaqing
# 2013.12.21
SERVER_ROOT='\/home\/jiaqing\/webapps'
SUPERVISOR_CONF_DIR=/etc/supervisor/conf.d/
NGINX_CONF_DIR=/etc/nginx/sites-enabled/

USAGE="Usage: `basename $0` sub_domain"
[ $# -lt 1 ] && {
    echo $USAGE
    exit 1
}
SUB_DOMAIN=$1

replace_domain()
{
    [ -f $1 ] &&
    {
        sed -i "s/sub_domain/$SUB_DOMAIN/g" $1
        sed -i "s/server_root/$SERVER_ROOT/g" $1
    }
}

[ -d $SUB_DOMAIN ] && rm -rf $SUB_DOMAIN
cp -r seed $SUB_DOMAIN
cd $SUB_DOMAIN
replace_domain gunicorn_wiki.sh
replace_domain settings_local.py
replace_domain wiki.conf
replace_domain wiki.nginx

cd ..
[ -d ../$SUB_DOMAIN ] && rm -rf ../$SUB_DOMAIN

mv $SUB_DOMAIN ../
cd ../$SUB_DOMAIN

SUPERVISOR_CONF=$SUPERVISOR_CONF_DIR/$SUB_DOMAIN.conf
NGINX_CONF=$NGINX_CONF_DIR/$SUB_DOMAIN.nginx
[ -e $SUPERVISOR_CONF ] && rm $SUPERVISOR_CONF
[ -e $NGINX_CONF ] && rm $NGINX_CONF

SUPER=`readlink -f wiki.conf`
NGINX=`readlink -f wiki.nginx`
ln -s $SUPER $SUPERVISOR_CONF
ln -s $NGINX $NGINX_CONF

supervisorctl reread
supervisorctl update
supervisorctl restart $SUB_DOMAIN
nginx -s reload
