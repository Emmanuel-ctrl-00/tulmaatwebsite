from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("booking/", views.booking, name="booking"),
    path("success/", views.success, name="success"),
]
