from django.urls import include
from django.urls import path

from apps.authentication import views

urlpatterns = [
    path(r"register/", views.register, name="register"),
]
