import os
from glob import glob

from django.shortcuts import render

PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, ".."))
PY_REPO_DIR = os.path.dirname(PY_ROOT_DIR)
CONFIG_DIR = r"config"


def index(request):
    path = os.path.join(PY_REPO_DIR, CONFIG_DIR)
    configs = [os.path.split(file)[-1]
               for p, subdir, files in os.walk(path)
               for file in glob(os.path.join(p, "*.yml"))]
    configs = [config for config in configs if ("chain" in config) & (config[:1] != "_")]

    return render(request, "run_chain/index.html", {'configs': configs})


def run(request, model_id):
    return render(request, "run_chain/run.html", context={'model_id': model_id})
