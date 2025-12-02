from django.urls import path
from . import views

app_name = "uploader"

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload, name="upload"),
    path("query/", views.query, name="query"),
]
