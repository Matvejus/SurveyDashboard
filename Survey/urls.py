"""Defines URL patterns."""

from django.urls import path

from . import views

app_name = "Survey"
urlpatterns = [
    # Home page
    path("", views.index, name="index"),
]
