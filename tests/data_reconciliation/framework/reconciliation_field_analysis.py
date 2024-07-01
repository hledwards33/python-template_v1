import logging

import numpy as np
import pandas as pd

from src.framework.setup.log_format import headers, no_format

logger = logging.getLogger()


def get_fields(main_data: pd.DataFrame, schema: dict) -> tuple[list, list]:
    numeric_fields = [key for key, val in schema.items() if
                      (isinstance(val, pd.Float64Dtype) | isinstance(val, pd.Int64Dtype))]
    numeric_fields = list(set(numeric_fields).intersection(set(main_data.columns)))

    string_fields = [key for key, val in schema.items() if val in ['string', 'object']]
    string_fields = list(set(string_fields).intersection(set(main_data.columns)))

    return numeric_fields, string_fields


def drop_fields(data: list, fields: list):
    updated_data = []
    for df in data:
        updated_data += [df.drop(columns=fields)]

    return updated_data


def detailed_numeric_analysis(main_data: pd.DataFrame, test_data: pd.DataFrame,
                              numeric_fields: list) -> tuple[pd.DataFrame, pd.DataFrame]:
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

    main_data, test_data = drop_fields([main_data, test_data], numeric_fields)

    return main_data, test_data


def detailed_string_analysis(main_data: pd.DataFrame, test_data: pd.DataFrame, string_fields: list) -> None:
    for field in string_fields:
        main_freq = main_data[field].astype('object').value_counts(dropna=False).sort_index()
        test_freq = test_data[field].astype('object').value_counts(dropna=False).sort_index()

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


def field_comparison(main_data: pd.DataFrame, test_data: pd.DataFrame, schema: dict) -> None:
    headers(" Field Reconciliation Results")

    numeric_fields, string_fields = get_fields(main_data, schema)

    # Analyse the numeric fields in detail
    main_data, test_data = detailed_numeric_analysis(main_data, test_data, numeric_fields)

    # Analyse the string fields in detail
    detailed_string_analysis(main_data, test_data, string_fields)
