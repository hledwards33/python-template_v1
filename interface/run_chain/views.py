import os

from django.shortcuts import render

PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, ".."))
PY_REPO_DIR = os.path.dirname(PY_ROOT_DIR)
WRAPPER_DIR = r"src/models/model_wrappers"


def index(request):
    path = os.path.join(PY_REPO_DIR, WRAPPER_DIR)
    wrappers = [file for file in os.listdir(path) if ((file[:1] != "_") & ("chain" in file))]

    return render(request, "run_chain/index.html", {'wrappers': wrappers})


def run(request, model_id):
    return render(request, "run_model/run.html", context={'model_id': model_id})
