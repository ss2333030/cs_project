from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name=""),
    path("list", views.list, name="list"),
    path("info", views.list, name="info"),
]
