from src.framework.setup.read_write_data import *


def test_read_json():
    test_json_path = r"C:\Users\GV147BE\PycharmProjects\python-template\tests\unit_tests\test_read_write_data\test_data"
    test_json_file = r"test_json.json"
    result = read_json((test_json_path, test_json_file))

    expected = {"first_key": 1, "second_key": "two"}

    assert result == expected
