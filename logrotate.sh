#!/usr/bin/env bash

if [ ! -d '/home/web/my_health_diary/logs' ]; then
    mkdir /home/web/my_health_diary/logs
fi

if [ ! -d '/home/web/my_health_diary/database' ]; then
    mkdir /home/web/my_health_diary/database
fi

if [ ! -d '/var/log/my_health_diary' ]; then
    mkdir /var/log/my_health_diary
   chown root /var/log/my_health_diary
fi

if [ ! -f '/etc/logrotate.d/my_health_diary' ]; then
   echo "/var/log/my_health_diary/*.log {
       su root root
       daily
       missingok
       rotate 5
       copytruncate
       compress
       delaycompress
       size 2M
   }" >> /etc/logrotate.d/my_health_diary
fi

logrotate -fv /etc/logrotate.d/my_health_diary
