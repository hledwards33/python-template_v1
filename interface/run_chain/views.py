import os
import sys
from glob import glob

import yaml
from django.shortcuts import render

PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, ".."))
PY_REPO_DIR = os.path.dirname(PY_ROOT_DIR)
CONFIG_DIR = r"config/model_config/model_chains"

sys.path.append(os.path.join(PY_REPO_DIR, "src"))
from framework.model_chain import ModelChain


def index(request):
    path = os.path.join(PY_REPO_DIR, CONFIG_DIR)
    configs = [file
               for p, subdir, files in os.walk(path)
               for file in glob(os.path.join(p, "*.yml"))]

    model_info = []
    for num, item in enumerate(configs):
        with open(item, "r") as file:
            params = yaml.safe_load(file)

            model_info += [{'index': num + 1,
                            'config_file': os.path.split(item)[-1],
                            'models_in_chain': params['models'].keys()}]

    return render(request, "run_chain/index.html", {'configs': model_info})


def run(request, model_id):
    path = os.path.join(PY_REPO_DIR, CONFIG_DIR)
    path = [file
            for p, subdir, files in os.walk(path)
            for file in glob(os.path.join(p, "*.yml")) if model_id == os.path.split(file)[-1][:-4]][0]

    run_chain(path, request)

    return render(request, "run_chain/run.html", context={'model_id': model_id})


def run_chain(path, request):
    model_chain = ModelChain(path)

    model_chain.run_chain()
