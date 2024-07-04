import pytest

from src.framework.setup.read_write_data import *

"""
Define fixed data to be used across tests
"""


@pytest.fixture
def schema():
    # Arrange
    return {"column_1": "float", "column_2": "string", "column_3": "integer", "column_4": "date"}


@pytest.fixture()
def integer_dataframe():
    # Arrange
    arr1 = pd.Series([1, 2, np.nan], dtype=pd.Int64Dtype())
    arr2 = pd.Series([np.nan, np.nan, np.nan], dtype=pd.Int64Dtype())
    arr3 = pd.Series([1, 2, 3], dtype=pd.Int64Dtype())

    df = pd.concat([arr1, arr2, arr3], axis=1)
    df.rename(columns={0: "integer_column_1", 1: "integer_column_2", 2: "integer_column_3"}, inplace=True)

    return df


@pytest.fixture()
def float_dataframe():
    # Arrange
    return pd.DataFrame({
        "float_column_1": [2.1, 1.2, 5.0],
        "float_column_2": [1, 2, 3],
        "float_column_3": [np.nan, 3.0, 1],
        "float_column_4": [np.nan, np.nan, np.nan]
    }, dtype=pd.Float64Dtype)


@pytest.fixture
def date_dataframe():
    # Arrange
    return pd.DataFrame({"date_column_1": ['04-10-1997', '06-10-2000', '12-12-1998'],
                         "date_column_2": [pd.NaT, '03-07-2024', '01-01-2022']}, dtype='datetime64[s]')


@pytest.fixture
def string_dataframe():
    # Arrange
    return pd.DataFrame({"string_column_1": ["", "", ""],
                         "string_column_2": ["test", "test", "test"],
                         "string_column_3": ["", "test", ""]}, dtype='string')


@pytest.fixture
def dataframe(integer_dataframe, float_dataframe, string_dataframe, date_dataframe):
    # Arrange
    return pd.concat([integer_dataframe, float_dataframe, string_dataframe, date_dataframe], axis=1)


@pytest.fixture
def dataframe_schema():
    # Arrange
    return {
        "integer_column_1": 'integer', "integer_column_2": 'integer', "integer_column_3": 'integer',
        "float_column_1": 'float', "float_column_2": 'float', "float_column_3": 'float',
        "float_column_4": 'float', "string_column_1": 'string', "string_column_2": 'string',
        "string_column_3": 'string', "date_column_1": 'date', "date_column_2": 'date'
    }


"""
Unit tests for functions contained within the src.framework.set.read_write_data
"""


def test_read_json_1():
    # Arrange
    from tests.unit_tests import test_data
    test_json_path = (test_data, "test_json.json")

    # Act
    result = read_json(test_json_path)

    # Assert
    expected = {"first_key": 1, "second_key": "two"}
    assert result == expected


def test_read_json_abs_1():
    # Arrange
    test_json_path = r"C:\Users\GV147BE\PycharmProjects\python-template\tests\unit_tests\test_data\test_json.json"

    # Act
    result = read_json_abs(test_json_path)

    # Assert
    expected = {"first_key": 1, "second_key": "two"}
    assert result == expected


def test_read_yaml_1():
    # Arrange
    test_yaml_path = r"C:\Users\GV147BE\PycharmProjects\python-template\tests\unit_tests\test_data\test_yaml.yaml"

    # Act
    result = read_yaml(test_yaml_path)

    # Assert
    expected = {"header": {"first_key": 1, "second_key": "two"}}
    assert result == expected


def test_convert_schema_pandas_1(schema):
    # Act
    result = convert_schema_pandas(schema)

    # Assert
    expected = {"column_1": pd.Float64Dtype(), "column_2": "string", "column_3": pd.Int64Dtype(),
                "column_4": 'datetime64[s]'}
    assert result == expected


def test_convert_schema_output_pandas_1(schema):
    # Act
    result = convert_schema_output_pandas(schema)

    # Assert
    expected = {"column_1": 'Float64', "column_2": "string", "column_3": 'Int64',
                "column_4": 'datetime64[s]'}
    assert result == expected


def test_convert_schema_recon_pandas_1(schema):
    # Act
    result = convert_schema_recon_pandas(schema)

    # Assert
    expected = {"column_1": pd.Float64Dtype(), "column_2": "string", "column_3": pd.Int64Dtype(),
                "column_4": 'string'}
    assert result == expected


def test_enforce_integers_1(integer_dataframe):
    # Act
    result = enforce_integers(integer_dataframe)

    # Assert
    expected = {"integer_column_1": 'float64', "integer_column_2": 'float64', "integer_column_3": 'int64'}
    assert result.dtypes.to_dict() == expected


def test_enforce_floats_1(float_dataframe):
    # Act
    result = enforce_floats(float_dataframe)

    # Assert
    expected = {"float_column_1": 'float64', "float_column_2": 'float64', "float_column_3": 'float64',
                "float_column_4": 'float64'}
    assert result.dtypes.to_dict() == expected


def test_enforce_strings_1(string_dataframe):
    # Act
    result = enforce_strings(string_dataframe)

    # Assert
    expected = {"string_column_1": 'string', "string_column_2": 'string', "string_column_3": 'string'}
    assert result.dtypes.to_dict() == expected


def test_enforce_data_types_1(dataframe):
    # Act
    dataframe.drop(columns=['date_column_1', 'date_column_2'], inplace=True)
    result = enforce_data_types(dataframe)

    # Assert
    expected = {"integer_column_1": 'float64', "integer_column_2": 'float64', "integer_column_3": 'int64',
                "float_column_1": 'float64', "float_column_2": 'float64', "float_column_3": 'float64',
                "float_column_4": 'float64', "string_column_1": 'string', "string_column_2": 'string',
                "string_column_3": 'string'}
    assert result.dtypes.to_dict() == expected


def test_schema_conformance_pandas_1(dataframe, dataframe_schema, caplog):
    """
    Testing the ability to identify extra column in the data that are not present in the schema
    """
    # Act
    dataframe_schema = convert_schema_output_pandas(dataframe_schema)
    for key in ['float_column_1', 'string_column_1']:
        dataframe_schema.pop(key)

    result = schema_conformance_pandas(dataframe, dataframe_schema, "test_schema_conformance_1")

    # Assert
    expected = ['float_column_1', 'string_column_1']
    assert (expected[0] in caplog.messages[0]) & (expected[1] in caplog.messages[0])


def test_schema_conformance_pandas_2(dataframe, dataframe_schema):
    """
    Testing the ability to identify a missing column in the dataset
    """
    # Act
    dataframe_schema = convert_schema_output_pandas(dataframe_schema)
    dataframe.drop(columns=['float_column_1', 'string_column_1'], inplace=True)
    result = schema_conformance_pandas(dataframe, dataframe_schema)

    # Assert
    expected = ['float_column_1', 'string_column_1']
    assert (expected[0] in result['missing_columns'][0]) & (expected[1] in result['missing_columns'][0])


def test_schema_conformance_pandas_3(dataframe, dataframe_schema):
    """
    Testing the ability to identify incorrect datatypes in the dataset
    """
    # Act
    dataframe_schema = convert_schema_output_pandas(dataframe_schema)
    dataframe_schema['integer_column_1'] = "float"
    dataframe_schema['date_column_1'] = "float"
    result = schema_conformance_pandas(dataframe, dataframe_schema)

    # Assert
    expected = ['Dataframe  has incorrect datatype in integer_column_1 expected float got Int64.',
                'Dataframe  has incorrect datatype in date_column_1 expected float got datetime64[s].']
    assert result['incorrect_type'] == expected


def test_read_csv_to_pandas_1():
    pass


def test_read_parquet_to_pandas_1():
    pass
