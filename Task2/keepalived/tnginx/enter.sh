#!/bin/sh


/usr/sbin/keepalived -n -l -D -f /etc/keepalived/keepalived.conf &
nginx -g "daemon off;"
