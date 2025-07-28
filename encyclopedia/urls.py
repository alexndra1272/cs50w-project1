from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new-page/", views.newPage, name="newPage")
]
