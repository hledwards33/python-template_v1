import datetime
import logging
import os

import pandas as pd

from src.framework.setup import read_write_data
from src.framework.setup.log_format import (create_logging_file, remove_handler, create_logging_file_handler_simple,
                                            initiate_logger, headers)
from tests.data_reconciliation.framework.reconciliation_data_analysis import data_comparison
from tests.data_reconciliation.framework.reconciliation_field_analysis import field_comparison

initiate_logger()
logger = logging.getLogger()

PY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PY_ROOT_DIR = os.path.abspath(os.path.join(PY_FILE_DIR, ".."))
PY_REPO_DIR = os.path.dirname(os.path.dirname(PY_ROOT_DIR))


def get_data_dir(sys_config) -> os.path:
    return os.path.join(PY_REPO_DIR, sys_config['data']['data_folder'])


def get_schema(path: str) -> dict:
    schema_path = os.path.join(PY_REPO_DIR, path)

    schema = read_write_data.read_json_abs(schema_path)

    schema = read_write_data.convert_schema_recon_pandas(schema)

    return schema


def get_data(path: str, schema: dict, sys_config: dict, usecols: bool = True) -> pd.DataFrame:
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


def use_matching_columns(df1: pd.DataFrame, df2: pd.DataFrame,
                         schema: dict) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    # Remove columns not in the intersection of both datasets
    df1 = df1.drop(columns=list(set(df1.columns).difference(set(df2.columns))))
    df2 = df2.drop(columns=list(set(df2.columns).difference(set(df1.columns))))

    # Remove columns from the schema
    schema = {key: val for key, val in schema.items() if key in df1.columns}

    return df1, df2, schema


def start_logging(config: dict, data_name: str) -> None:
    name = config['log_name']
    path = os.path.join(PY_REPO_DIR, config['log_location'])
    create_logging_file(create_logging_file_handler_simple, path, name, data_name=data_name)


def get_args(log_config: dict, usecols: bool = False, matching_columns: bool = False, remove_columns: list = [],
             verbose: bool = True) -> tuple[bool, bool, list, bool]:
    try:
        usecols = log_config['usecols']
    except KeyError:
        log_config['use_cols'] = usecols

    try:
        matching_columns = log_config['matching_columns']
    except KeyError:
        log_config['matching_columns'] = matching_columns

    try:
        remove_columns = log_config['remove_columns']
    except KeyError:
        log_config['remove_columns'] = remove_columns

    try:
        verbose = log_config['verbose']
    except KeyError:
        log_config['verbose'] = verbose

    return usecols, matching_columns, remove_columns, verbose


def config_logs(log_config: dict) -> None:
    headers("Reconciliation Configuration")

    logger.info(f"This log was created {datetime.date.today()} {datetime.datetime.now().strftime('%H:%M:%S')}.")
    logging.info(f"Reconciliation Results file pattern: {log_config['log_location']}/{log_config['log_name']}.")

    for key, val in log_config.items():
        if key not in ['log_location', 'log_name']:
            logging.info(f"Parameter {key} has been set to {val} for the creation of the below logs.")


def apply_data_choices(main_data: pd.DataFrame, test_data: pd.DataFrame, matching_columns: bool,
                       remove_columns: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    if matching_columns:
        logger.info("Only common columns between both datasets are being compared.")
        main_data, test_data, schema = use_matching_columns(main_data, test_data, schema)

    if remove_columns:
        logger.info(f"The following columns have been removed from the analysis: {remove_columns}.")
        main_data = main_data.drop(columns=remove_columns, inplace=True)
        test_data = test_data.drop(columns=remove_columns, inplace=True)

    return main_data, test_data


def load_main_and_test_data(data_config: dict, sys_config: dict, schema: dict, usecols: bool, matching_columns: bool,
                            remove_columns: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    main_data = get_data(data_config['main_data_path'], schema, sys_config, usecols=usecols)

    test_data = get_data(data_config['test_data_path'], schema, sys_config, usecols=usecols)

    main_data, test_data = apply_data_choices(main_data, test_data, matching_columns,
                                              remove_columns)

    return main_data, test_data


def set_up_data(data_config: dict, sys_config: dict, data: str, usecols: bool, matching_columns: bool,
                remove_columns: list) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    headers(f"{data.upper()} Data Reconciliation")

    schema = get_schema(data_config['schema_path'])

    headers("Reading Input Data")

    main_data, test_data = load_main_and_test_data(data_config, sys_config, schema,
                                                   usecols, matching_columns, remove_columns)

    return main_data, test_data, schema


def run_full_data_reconciliation(sys_config_path: str, recon_config_path: str) -> None:
    sys_config = read_write_data.read_yaml(os.path.join(PY_REPO_DIR, sys_config_path))
    recon_config = read_write_data.read_yaml(os.path.join(PY_REPO_DIR, recon_config_path))
    log_config = recon_config['config'].copy()
    del recon_config['config']

    usecols, matching_columns, remove_columns, verbose = get_args(log_config)

    for data, data_config in recon_config.items():

        start_logging(log_config, data)

        config_logs(log_config)

        main_data, test_data, schema = set_up_data(data_config, sys_config, data,usecols,
                                                   matching_columns, remove_columns)

        match, main_data, test_data = data_comparison(schema, main_data, test_data,
                                                      verbose=verbose)

        if not match:
            field_comparison(main_data, test_data, schema)

        remove_handler(data)
