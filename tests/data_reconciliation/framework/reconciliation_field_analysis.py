import logging

import numpy as np
import pandas as pd

from src.framework.setup.log_format import headers, no_format

logger = logging.getLogger()


def field_comparison(main_data: pd.DataFrame, test_data: pd.DataFrame, schema: dict):
    headers(" Field Reconciliation Results")

    numeric_fields = [key for key, val in schema.items() if
                      (isinstance(val, pd.Float64Dtype) | isinstance(val, pd.Int64Dtype))]
    numeric_fields = list(set(numeric_fields).intersection(set(main_data.columns)))

    string_fields = [key for key, val in schema.items() if val == 'object']
    string_fields = list(set(string_fields).intersection(set(main_data.columns)))

    # Analyse the numeric fields in detail
    for field in numeric_fields:
        if main_data[field].sum() == 0:
            percent_diff = 100
        else:
            percent_diff = (main_data[field].sum() - test_data[field].sum()) / main_data[field].sum() * 100

        headers(field.upper())
        logger.info(f"The main data field sum is {main_data[field].sum()}.")
        logger.info(f"The test data field sum is {test_data[field].sum()}.")
        logger.info(f"The difference between the datasets is "
                    f"{main_data[field].sum() - test_data[field].sum()}.")
        logger.info(f"The % difference between the datasets is {percent_diff}%.")

    # Analyse the string fields in detail
    for field in string_fields:
        main_freq = main_data[field].value_counts(dropna=False).sort_index()
        test_freq = test_data[field].value_counts(dropna=False).sort_index()

        difference = main_freq - test_freq
        difference = difference.rename_axis('value').reset_index(name='count')
        difference = difference.loc[difference['count'] != 0].copy()

        difference['count'] = np.where(difference['count'].isna(),
                                       np.where(difference['value'].isin(list(main_freq.index)),
                                                "In Main Data Only", "In Test Data Only"),
                                       difference['count'])

        headers(field.upper())

        logger.info("The differences between the datasets are:")
        no_format(difference.rename(columns={'count': 'main v test'}))
