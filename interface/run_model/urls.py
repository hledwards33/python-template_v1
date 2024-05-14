from django.urls import path

from . import views

app_name = "run_model"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:model_id>/", views.run, name="run"),
    path("repo_info", views.repo, name="repo")
]
