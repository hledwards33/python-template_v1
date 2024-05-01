import os

from src.framework.setup import read_write_data
from tests.data_reconciliation.framework.reconciliation_data_analysis import data_comparison

recon_config_path = r"models/example_model/example_model_reconciliation.yml"
sys_config_path = r"config/system_config.yml"

PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, ".."))
PY_REPO_DIR = os.path.dirname(os.path.dirname(PY_ROOT_DIR))

sys_config = read_write_data.read_yaml(os.path.join(PY_REPO_DIR, sys_config_path))
recon_config = read_write_data.read_yaml(os.path.join(PY_ROOT_DIR, recon_config_path))


def get_data_dir(sys_config):
    return os.path.join(PY_REPO_DIR, sys_config['data']['data_folder'])


def get_schema(path: str) -> dict:
    schema_path = os.path.join(PY_REPO_DIR, path)

    schema = read_write_data.read_json_abs(schema_path)

    schema = read_write_data.convert_schema_recon_pandas(schema)

    return schema


def get_data(path: str, sys_config: dict):

    file_type = path.split(".")[-1]
    path = os.path.join(get_data_dir(sys_config), path)

    if file_type in ["csv", "zip"]:

        data = read_write_data.read_csv_to_pandas(path=path, schema=schema)

    elif file_type in ["pqt", "parquet"]:

        data = read_write_data.read_parquet_to_pandas(path=path, schema=schema)

    else:
        raise ImportError('Incorrect data path supplied in config.')

    return data


for data, data_config in recon_config.items():
    schema = get_schema(data_config['schema_path'])

    main_data = get_data(data_config['main_data_path'], sys_config)

    test_data = get_data(data_config['test_data_path'], sys_config)

    data_comparison(schema, main_data, test_data)

print("Done!")
