from django.urls import path

from . import views

app_name = "run_chain"
urlpatterns = [
    path("", views.index, name="index"),
]
