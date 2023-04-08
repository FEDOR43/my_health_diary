import os

from celery import Celery

from my_health_diary import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_health_diary.settings")
app = Celery("my_health_diary")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    "send-queued-mail": {
        "task": "post_office.tasks.send_queued_mail",
        "schedule": 600.0,
    },
}
