from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("booking.html/", views.booking, name="booking"),
    path("success.html/", views.success, name="success"),
]