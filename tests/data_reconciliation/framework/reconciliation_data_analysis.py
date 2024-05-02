import logging

import numpy as np
import pandas as pd

from framework.setup.log_format import headers

logger = logging.getLogger()


def data_comparison(schema, main_data: pd.DataFrame, test_data: pd.DataFrame, verbose: bool = True):
    headers("Reconciliation Results")

    numeric_fields = [key for key, val in schema.items() if
                      (isinstance(val, pd.Float64Dtype) | isinstance(val, pd.Int64Dtype))]
    string_fields = [key for key, val in schema.items() if val == 'object']

    error_count = 0
    numeric_errors = []
    string_errors = []
    total_fields = len(main_data.columns)

    if len(main_data) != len(test_data):
        raise ValueError(f"ERROR: Datasets do not have the same number of rows. Main data has {len(main_data)} rows, "
                         f"test data has {len(test_data)} rows.")
    else:
        logger.info(f"Both datasets have {len(main_data)} rows.")

    if len(main_data.columns) != len(main_data.columns):
        raise ValueError(f"ERROR: The datasets do not have the same number of columns. "
                         f"Main data has {len(main_data.columns)} columns, "
                         f"test data has {len(test_data.columns)} columns. "
                         f"Main data has extra columns {set(main_data.columns).difference(set(test_data.columns))}. "
                         f"Test data has extra columns {set(test_data.columns).difference(set(main_data.columns))}.")
    else:
        logger.info(f"Both datasets have {len(main_data.columns)} columns.")

    # Compare the totals of the numeric fields
    for field in numeric_fields:
        if (test_data[field].sum() == 0 or np.isnan(test_data[field].sum())) and (
                main_data[field].sum() != 0 and not np.isnan(main_data[field].sum())):
            difference = 1
        elif main_data[field].sum() == 0 or np.isnan(main_data[field].sum()):
            difference = (main_data[field].sum() - test_data[field].sum())
        else:
            difference = ((main_data[field].sum() - test_data[field].sum()) / main_data[field].sum())

        if abs(difference) > 0.00001:
            logger.info(f"ERROR: The {field} field does nt match the difference is"
                        f"{main_data[field].sum() - test_data[field].sum()}.")

            error_count += 1
            numeric_errors += [field]
        else:
            if verbose:
                logger.info(f"Both {field} fields have sum {main_data[field].sum()}.")

    # Check for differences in the number of null values in numeric columns
    errors = {}
    for field in numeric_fields:
        main_nulls = sum(main_data[field].isna())
        test_nulls = sum(test_data[field].isna())
        difference = main_nulls - test_nulls

        if difference == 0:
            continue
        elif difference > 0:
            errors[field] = [f"The field {field} has {difference} more null values in the main data than in the test "
                             f"data. {main_nulls} in main data, {test_nulls} in test data.", 1]
        elif difference < 0:
            errors[field] = [f"The field {field} has {difference} more null values in the test data than in the main "
                             f"data. {main_nulls} in main data, {test_nulls} in test data.", -1]

    # Drop numeric fields that are not throwing errors
    main_data = main_data.drop(columns=list(set(numeric_fields).difference(set(numeric_errors))))
    test_data = test_data.drop(columns=list(set(numeric_fields).difference(set(numeric_errors))))

    # Check for differences in frequencies in string fields
    for field in string_fields:
        main_freq = main_data[field].value_counts(dropna=False)
        main_freq.index = main_freq.index.astype(str, copy=False)
        main_freq.sort_index(inplace=False)

        test_freq = main_data[field].value_counts(dropna=False)
        test_freq.index = test_freq.index.astype(str, copy=False)
        test_freq.sort_index(inplace=False)

        difference = sum(main_freq - test_freq)

        if difference != 0:
            logger.info(f"ERROR: The {field} does not have consistent values.")
            error_count += 1
            string_errors += [field]
        else:
            if verbose:
                logger.info(f"Both {field} fields have the same value frequencies.")

    # Drop string fields that are not throwing errors
    main_data = main_data.drop(columns=list(set(string_fields).difference(set(string_errors))))
    test_data = test_data.drop(columns=list(set(string_fields).difference(set(string_errors))))

    headers("Results Summary")

    if error_count > 0:
        logger.info(fr"The datasets do not reconcile with each other, there are {error_count}\{total_fields} errors.")
        logger.info(f"Numeric Error Fields: {numeric_errors}")
        logger.info(f"String Error Fields: {string_errors}")
    else:
        logger.info(f"The datasets reconcile with each other, all {total_fields} fields match.")

    headers("Numeric Null Summary")

    if len(errors) > 0:
        logger.info(fr"There are {len(errors)}\{len(numeric_fields)} numeric fields with differing numbers of"
                    f"null values.")
        logger.info(f"Main data has more nulls for fields: {[k for k, v in errors.items() if v[1] == 1]}")
        logger.info(f"Test data has more nulls for fields: {[k for k, v in errors.items() if v[1] == -1]}")
    else:
        logger.info("There are no differences in the number of numeric nulls between the datasets.")

    if len(errors) > 0:
        headers("Numeric Nulls Results")
        for val in errors.values():
            logger.info(val[0])

    match = True if error_count == 0 else False

    return match, main_data, test_data
