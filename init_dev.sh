#!/bin/bash
# инициализация стартовых настроек при развёртывании нового проекта.
# перед запуском скрипта установить права на выполнение. chmod ugo+x init_dev.sh
# запуск: ./init_dev.sh

sudo chmod +x ./logrotate.sh
sudo chmod +x ./manage.py
sudo ./logrotate.sh
sudo ln -s /home/web/my_health_diary/conf.d/nginx/mhd_dev.conf /etc/nginx/conf.d/
sudo nginx -s reload

sudo docker-compose up -d --build
sudo docker-compose exec mhd_app python manage.py migrate
sudo docker-compose exec mhd_app python manage.py collectstatic
#sudo docker-compose exec mhd_app python manage.py database_init
