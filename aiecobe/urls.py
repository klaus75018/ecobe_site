from django.urls import path, include

from . import views



urlpatterns = [
    path('incendie', views.incendie, name = "incendie"),
    path('projects_overview', views.projects_overview, name = "projects_overview"),
]