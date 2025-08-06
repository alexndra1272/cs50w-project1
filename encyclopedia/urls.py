from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new-page/", views.new_page, name="new_page"),
    path("edit/<str:entry>/", views.edit_page, name="edit_page"),
    path("search/", views.search, name="search")
]
