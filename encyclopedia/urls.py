from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.openpage, name="title"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("editform/<str:title>", views.editform, name="editform"),
    path("pushedit", views.pushedit, name="pushedit"),
    path("randompage", views.randompage, name="randompage")
]
