import logging

import numpy as np
import pandas as pd

from src.framework.setup.log_format import headers

logger = logging.getLogger()


def get_fields(main_data: pd.DataFrame, schema: dict) -> tuple[list, list, int]:
    numeric_fields = [key for key, val in schema.items() if
                      (isinstance(val, pd.Float64Dtype) | isinstance(val, pd.Int64Dtype))]
    string_fields = [key for key, val in schema.items() if val in ['string', 'object']]

    total_fields = len(main_data.columns)

    return numeric_fields, string_fields, total_fields


def test_length(main_data: pd.DataFrame, test_data: pd.DataFrame) -> None:
    if len(main_data) != len(test_data):
        raise ValueError(f"ERROR: Datasets do not have the same number of rows. Main data has {len(main_data)} rows, "
                         f"test data has {len(test_data)} rows.")
    else:
        logger.info(f"Both datasets have {len(main_data)} rows.")


def test_width(main_data: pd.DataFrame, test_data: pd.DataFrame) -> None:
    if len(main_data.columns) != len(main_data.columns):
        raise ValueError(f"ERROR: The datasets do not have the same number of columns. "
                         f"Main data has {len(main_data.columns)} columns, "
                         f"test data has {len(test_data.columns)} columns. "
                         f"Main data has extra columns {set(main_data.columns).difference(set(test_data.columns))}. "
                         f"Test data has extra columns {set(test_data.columns).difference(set(main_data.columns))}.")
    else:
        logger.info(f"Both datasets have {len(main_data.columns)} columns.")


def test_dimensions(main_data: pd.DataFrame, test_data: pd.DataFrame) -> None:
    test_length(main_data, test_data)

    test_width(main_data, test_data)


def test_numeric_fields(main_data: pd.DataFrame, test_data: pd.DataFrame, numeric_fields: list, verbose: bool,
                        error_count: int, numeric_errors: list) -> tuple[int, list]:
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

        return error_count, numeric_errors


def test_numeric_nulls(main_data: pd.DataFrame, test_data: pd.DataFrame, numeric_fields: list) -> dict:
    null_errors = {}

    for field in numeric_fields:
        main_nulls = sum(main_data[field].isna())
        test_nulls = sum(test_data[field].isna())
        difference = main_nulls - test_nulls

        if difference == 0:
            continue
        elif difference > 0:
            null_errors[field] = [
                f"The field {field} has {difference} more null values in the main data than in the test "
                f"data. {main_nulls} in main data, {test_nulls} in test data.", 1]
        elif difference < 0:
            null_errors[field] = [
                f"The field {field} has {difference} more null values in the test data than in the main "
                f"data. {main_nulls} in main data, {test_nulls} in test data.", -1]

    return null_errors


def test_string_fields(main_data: pd.DataFrame, test_data: pd.DataFrame, string_fields: list, verbose: bool,
                       error_count: int, string_errors: list) -> tuple[int, list]:
    for field in string_fields:
        main_freq = main_data[field].astype('object').value_counts(dropna=False)
        main_freq.index = main_freq.index.astype(str, copy=False)
        main_freq.sort_index(inplace=False)

        test_freq = test_data[field].astype('object').value_counts(dropna=False)
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

        return error_count, string_errors


def test_values(schema: dict, main_data: pd.DataFrame, test_data: pd.DataFrame,
                verbose: bool = True) -> tuple[pd.DataFrame, pd.DataFrame, list]:
    # Split fields by category
    numeric_fields, string_fields, total_fields = get_fields(main_data, schema)

    # Initiate counting / holding variables
    error_count, numeric_errors, string_errors = 0, [], []

    # Check if the dimensions of the dataframes match
    test_dimensions(main_data, test_data)

    # Compare the totals of the numeric fields
    error_count, numeric_errors = test_numeric_fields(main_data, test_data, numeric_fields,
                                                      verbose, error_count, numeric_errors)

    # Check for differences in the number of null values in numeric columns
    null_errors = test_numeric_nulls(main_data, test_data, numeric_fields)

    # Drop numeric fields that are not throwing errors
    main_data, test_data = drop_matching_columns([main_data, test_data], numeric_fields, numeric_errors)

    # Check for differences in frequencies in string fields
    error_count, string_errors = test_string_fields(main_data, test_data, string_fields,
                                                    verbose, error_count, string_errors)

    # Drop string fields that are not throwing errors
    main_data, test_data = drop_matching_columns([main_data, test_data], string_fields, string_errors)

    return main_data, test_data, [total_fields, numeric_fields, error_count, string_errors, numeric_errors, null_errors]


def drop_matching_columns(data: list, fields: list, fields_to_keep: list) -> list:
    updated_data = []
    for df in data:
        updated_data += [df.drop(columns=list(set(fields).difference(set(fields_to_keep))))]

    return updated_data


def summarise_errors(error_count: int, total_fields: int, numeric_errors: list, string_errors: list) -> None:
    if error_count > 0:
        logger.info(fr"The datasets do not reconcile with each other, there are {error_count}\{total_fields} errors.")
        logger.info(f"Numeric Error Fields: {numeric_errors}")
        logger.info(f"String Error Fields: {string_errors}")
    else:
        logger.info(f"The datasets reconcile with each other, all {total_fields} fields match.")


def summarise_null_errors(null_errors: dict, numeric_fields: list) -> None:
    if len(null_errors) > 0:
        logger.info(fr"There are {len(null_errors)}\{len(numeric_fields)} numeric fields with differing numbers of"
                    f"null values.")
        logger.info(f"Main data has more nulls for fields: {[k for k, v in null_errors.items() if v[1] == 1]}")
        logger.info(f"Test data has more nulls for fields: {[k for k, v in null_errors.items() if v[1] == -1]}")
    else:
        logger.info("There are no differences in the number of numeric nulls between the datasets.")

    if len(null_errors) > 0:
        headers("Numeric Nulls Results")
        for val in null_errors.values():
            logger.info(val[0])


def summarise_test_outcome(test_result: list) -> bool:
    # Unpack the test results into variables
    total_fields, numeric_fields, error_count, string_errors, numeric_errors, null_errors = test_result

    summarise_errors(error_count, total_fields, numeric_errors, string_errors)

    headers("Numeric Null Summary")

    summarise_null_errors(null_errors, numeric_fields)

    match = True if error_count == 0 else False

    return match


def data_comparison(schema: dict, main_data: pd.DataFrame, test_data: pd.DataFrame,
                    verbose: bool = True) -> tuple[bool, pd.DataFrame, pd.DataFrame]:
    headers("Data Reconciliation Results")
    # Compare the two datasets
    main_data, test_data, test_result = test_values(schema, main_data, test_data, verbose)

    headers("Results Summary")
    # Summarise the comparison outcome
    match = summarise_test_outcome(test_result)

    return match, main_data, test_data
