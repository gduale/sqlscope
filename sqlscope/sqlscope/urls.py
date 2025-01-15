from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("about/", views.about, name="about"),
    path("engine-parameters/", views.engine_parameters, name="engine_parameters"),
    path("databases/", views.databases, name="databases"),
]
