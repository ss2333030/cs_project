from django.urls import path
from . import views


app_name = ""
urlpatterns = [
    path("", views.index, name="index"),
    path("list", views.list, name="list"),
    path("info", views.info, name="info"),
]
