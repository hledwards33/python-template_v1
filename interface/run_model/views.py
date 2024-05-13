import os
from glob import glob
import sys

from django.shortcuts import render

PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, ".."))
PY_REPO_DIR = os.path.dirname(PY_ROOT_DIR)
WRAPPER_DIR = r"src/models/model_wrappers"

sys.path.append(os.path.join(PY_REPO_DIR, "src"))


def index(request):
    path = os.path.join(PY_REPO_DIR, WRAPPER_DIR)
    wrappers = [file for file in os.listdir(path) if ((file[:1] != "_") & ("chain" not in file))]

    return render(request, "run_model/index.html", {'wrappers': wrappers})


def run(request, model_id):
    path = os.path.join(PY_REPO_DIR, WRAPPER_DIR)
    path = [file
            for p, subdir, files in os.walk(path)
            for file in glob(os.path.join(p, "*.py")) if model_id == os.path.split(file)[-1][:-3]][0]

    f = open(path, "r")
    print(f)

    return render(request, "run_model/run.html", context={'model_id': model_id})
