FROM my_health_diary_backend:latest

WORKDIR /srv/app

COPY ./ ./

#CMD [ \
#    "sh", "-c", "rm -f ./*.pid ; \
#   celery multi start --app=config worker1 \
#   --pidfile=./celeryworker.pid \
#   --logfile=./logs/celeryworker.log --concurrency=2 --loglevel=WARNING ; \
#   celery --app=config beat \
#   --pidfile=./celerybeat.pid \
#   --logfile=./logs/celerybeat.log --loglevel=WARNING" \
#]
