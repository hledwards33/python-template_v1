"""
This script infers the datatypes of a given dataset to create a dataset schema.
"""
import pandas as pd


def create_schema(path: str) -> str:
    df = pd.read_csv(path)

    schema = pd.io.json.build_table_schema(df)

    schema = {d['name']: d['type'] for d in schema['fields'] if d['name'].lower() != 'index'}

    schema = {k: ('float' if v == 'number' else v) for k, v in schema.items()}

    print("Copy and Paste the below schema into desire schema json file.")
    print(schema)


if __name__ == "__main__":
    data_path = r"C:\Users\GV147BE\PycharmProjects\python-template\data\example_model\inputs\pd_data.csv"

    create_schema(data_path)
