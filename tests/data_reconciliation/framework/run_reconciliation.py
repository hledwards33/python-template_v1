import datetime
import logging
import os

import pandas as pd

from framework.setup.log_format import create_logging_file, remove_handler, create_logging_file_handler_simple
from src.framework.setup import read_write_data
from tests.data_reconciliation.framework.reconciliation_data_analysis import data_comparison

logger = logging.getLogger()

PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, ".."))
PY_REPO_DIR = os.path.dirname(os.path.dirname(PY_ROOT_DIR))


def get_data_dir(sys_config):
    return os.path.join(PY_REPO_DIR, sys_config['data']['data_folder'])


def get_schema(path: str) -> dict:
    schema_path = os.path.join(PY_REPO_DIR, path)

    schema = read_write_data.read_json_abs(schema_path)

    schema = read_write_data.convert_schema_recon_pandas(schema)

    return schema


def get_data(path: str, schema: dict, sys_config: dict, usecols: bool = True):
    file_type = path.split(".")[-1]
    path = os.path.join(get_data_dir(sys_config), path)

    if file_type in ["csv", "zip"]:

        data = read_write_data.read_csv_to_pandas(path=path, schema=schema, usecols=usecols)

    elif file_type in ["pqt", "parquet"]:

        data = read_write_data.read_parquet_to_pandas(path=path, schema=schema)

    else:
        raise ImportError('Incorrect data path supplied in config.')

    # Convert columns to lower case
    data.columns = [col.strip().lower() for col in data.columns]

    return data


def use_matching_columns(df1: pd.DataFrame, df2: pd.DataFrame, schema: dict) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    # Remove columns not in the intersection of both datasets
    df1 = df1.drop(columns=set(df1.columns).difference(set(df2.columns)))
    df2 = df2.drop(columns=set(df2.columns).difference(set(df1.columns)))

    # Remove columns from the schema
    schema = {key: val for key, val in schema.items() if key in df1.columns}

    return df1, df2, schema


def start_logging(config: dict, data_name: str):
    name = config['log_name']
    path = os.path.join(PY_REPO_DIR, config['log_location'])
    create_logging_file(create_logging_file_handler_simple, path, name, data_name=data_name)


def run_full_data_reconciliation(sys_config_path: str, recon_config_path: str,
                                 usecols: bool = False, matching_columns: bool = False, remove_columns: list = []):
    sys_config = read_write_data.read_yaml(os.path.join(PY_REPO_DIR, sys_config_path))
    recon_config = read_write_data.read_yaml(os.path.join(PY_REPO_DIR, recon_config_path))
    log_config = recon_config['outputs'].copy()
    del recon_config['outputs']

    for data, data_config in recon_config.items():

        start_logging(log_config, data)

        logger.info(f"Reconciliation of '{data.upper()}', date: {datetime.date.today()} "
                    f"{datetime.datetime.now().strftime('%H:%M:%S')}.")

        schema = get_schema(data_config['schema_path'])

        main_data = get_data(data_config['main_data_path'], schema, sys_config, usecols=usecols)

        test_data = get_data(data_config['test_data_path'], schema, sys_config, usecols=usecols)

        if matching_columns:
            logger.info("Only common columns between both datasets are being compared.")
            main_data, test_data, schema = use_matching_columns(main_data, test_data, schema)

        if remove_columns:
            logger.info(f"The following columns have been removed from the analysis: {remove_columns}.")
            main_data = main_data.drop(columns=remove_columns, inplace=True)
            test_data = test_data.drop(columns=remove_columns, inplace=True)

        data_comparison(schema, main_data, test_data)

        remove_handler(data)


if __name__ == "__main__":
    kwargs = {
        'sys_config_path': r"config/system_config.yml",
        'recon_config_path': r"config/model_config/example_model/example_model_reconciliation.yml",
        'usecols': False,
        'matching_columns': False,
        'remove_columns': []
    }

    run_full_data_reconciliation(**kwargs)

    print("Done!")
