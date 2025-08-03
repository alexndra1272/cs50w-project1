from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new-page/", views.new_page, name="new_page"),
    path("search/", views.search, name="search")
]
