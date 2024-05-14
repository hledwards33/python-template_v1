import datetime
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

    model_logs = run_chain(path, request)

    return render(request, "run_chain/run.html",
                  context={'model_id': model_id, 'model_logs': model_logs})


def run_chain(path, request):
    model_chain = ModelChain(path)

    model_chain.run_chain()

    # Get model logs for each model in the chain
    with open(path, 'r') as file:
        config = yaml.safe_load(file)['models']

    model_logs = {}
    for key, val in config.items():
        with open(os.path.join(PY_REPO_DIR, val['config']), 'r') as file:
            log_info = yaml.safe_load(file)['parameters']['model_parameters']

        log_name = log_info['log_name']
        if '{date}' in log_name:
            log_name = log_name.format(date=datetime.date.today())

        with open(os.path.join(PY_REPO_DIR, log_info['log_location'], log_name) + ".log", 'r') as file:
            logs = file.read().splitlines()

        model_logs[key] = logs

    return model_logs
