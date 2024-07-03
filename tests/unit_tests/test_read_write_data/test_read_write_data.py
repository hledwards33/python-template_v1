from src.framework.setup.read_write_data import *


def test_read_json_1():
    # Arrange
    from tests.unit_tests.test_read_write_data import test_data
    test_json_path = (test_data, "test_json.json")

    # Act
    result = read_json(test_json_path)

    # Assert
    expected = {"first_key": 1, "second_key": "two"}
    assert result == expected


def test_read_json_abs_1():
    # Arrange
    test_json_path = r"C:\Users\GV147BE\PycharmProjects\python-template\tests\unit_tests\test_read_write_data\test_data\test_json.json"

    # Act
    result = read_json_abs(test_json_path)

    # Assert
    expected = {"first_key": 1, "second_key": "two"}
    assert result == expected


def test_read_yaml_1():
    # Arrange
    test_yaml_path = r"C:\Users\GV147BE\PycharmProjects\python-template\tests\unit_tests\test_read_write_data\test_data\test_yaml.yaml"

    # Act
    result = read_yaml(test_yaml_path)

    # Assert
    expected = {"header": {"first_key": 1, "second_key": "two"}}
    assert result == expected
