import logging

import pandas as pd

logger = logging.getLogger()


def data_comparison(schema, main_data: pd.DataFrame, test_data: pd.DataFrame, use_cols: bool = False,
                    verbose: bool = True, remove_columns: list = [], only_matching_columns: bool = False):
    numeric_columns = [key for key, val in schema.items() if
                       (isinstance(val, pd.Float64Dtype) | isinstance(val, pd.Int64Dtype))]
    string_columns = [key for key, val in schema.items() if val == 'object']

    print("Done!")
