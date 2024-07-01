"""
This script zips all csv files in a folder into individual zip files.
"""

import os

import pandas as pd


def get_csvs(path: str) -> list:
    filenames = os.listdir(path)
    return [os.path.join(path, filename) for filename in filenames if filename.endswith(".csv")]


def convert_to_csv(file_paths: list) -> None:
    for path in file_paths:
        df = pd.read_csv(path, dtype=str)
        df.to_csv(path[:-4] + ".zip", compression={'method': 'zip'})


def all_files_to_csv(path: str) -> None:
    target_files = get_csvs(path)
    convert_to_csv(target_files)


if __name__ == "__main__":
    kwargs = {'path': r"C:\Users\GV147BE\PycharmProjects\python-template\data\example_model\inputs"}

    all_files_to_csv(**kwargs)

    print()
