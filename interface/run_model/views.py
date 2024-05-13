import os
import sys
from glob import glob

from django.shortcuts import render

PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, ".."))
PY_REPO_DIR = os.path.dirname(PY_ROOT_DIR)
CONFIG_DIR = r"config/model_config/model_metadata"

sys.path.append(os.path.join(PY_REPO_DIR, "src"))
from framework.model_wrapper import DeployWrapper


def index(request):
    path = os.path.join(PY_REPO_DIR, CONFIG_DIR)
    configs = [os.path.split(file)[-1]
               for p, subdir, files in os.walk(path)
               for file in glob(os.path.join(p, "*.yml"))]

    return render(request, "run_chain/index.html", {'configs': configs})


def run(request, model_id):
    path = os.path.join(PY_REPO_DIR, CONFIG_DIR)
    path = [file
            for p, subdir, files in os.walk(path)
            for file in glob(os.path.join(p, "*.yml")) if model_id == os.path.split(file)[-1][:-4]][0]

    model = DeployWrapper

    return render(request, "run_chain/run.html", context={'model_id': model_id})


def run_chain(path, request):
    model_chain = ModelChain(path)

    model_chain.run_chain()
