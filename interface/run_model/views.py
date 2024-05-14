import datetime
import importlib
import os
import sys
from glob import glob

import yaml
from django.contrib import messages
from django.shortcuts import render

PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, ".."))
PY_REPO_DIR = os.path.dirname(PY_ROOT_DIR)
CONFIG_DIR = r"config/model_config/model_metadata"

sys.path.append(os.path.join(PY_REPO_DIR, "src"))
sys.path.append(PY_REPO_DIR)
from framework.model_wrapper import DeployWrapper


def home(request):
    return render(request, "run_model/home.html")


def repo(request):
    return render(request, "run_model/repo.html")


def index(request):
    path = os.path.join(PY_REPO_DIR, CONFIG_DIR)
    configs = [file
               for p, subdir, files in os.walk(path)
               for file in glob(os.path.join(p, "*.yml"))]

    model_info = []
    for num, item in enumerate(configs):
        with open(item, "r") as file:
            params = yaml.safe_load(file)['config']

        model_info += [{'index': num + 1,
                        'config_file': os.path.split(item)[-1],
                        'model_id': params['model_id'],
                        'model_type': params['model_type'],
                        'type': params['type']}]

    return render(request, "run_model/index.html", {'configs': model_info})


def run(request, model_id):
    path = os.path.join(PY_REPO_DIR, CONFIG_DIR)
    path = [file
            for p, subdir, files in os.walk(path)
            for file in glob(os.path.join(p, "*.yml")) if model_id == os.path.split(file)[-1][:-4]][0]

    run_model(request, path)

    return render(request, "run_model/run.html", context={'model_id': model_id})


def run_model(request, path: str):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)['config']

    DeployWrapper(get_model_class(config), config['sys_config'],
                  config['model_config']).run_model()

    with open(os.path.join(PY_REPO_DIR, config['model_config'])) as file:
        config = yaml.safe_load(file)['parameters']['model_parameters']

    log_name = config['log_name']
    if '{date}' in log_name:
        log_name = log_name.format(date=datetime.date.today())

    with open(os.path.join(PY_REPO_DIR, config['log_location'], log_name) + ".log", 'r') as file:
        logs = file.read().splitlines()

    for line in logs:
        messages.add_message(request, messages.INFO, line)


def get_model_class(model_config: dict):
    model_class = getattr(importlib.import_module(model_config['model_path']), model_config['model'])
    return model_class
