FROM my_health_diary_backend:latest

COPY . .

EXPOSE 8090

CMD [ \
    "gunicorn", "-b", "0.0.0.0:8090", \
    "--timeout", "120", "-w", "4", "-k", "gthread", \
    "--threads", "4", "my_health_diary.wsgi:application" \
]
