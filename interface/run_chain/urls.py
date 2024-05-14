from django.urls import path

from . import views

app_name = "run_chain"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:model_id>/", views.run, name="run"),
]
