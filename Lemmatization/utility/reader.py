from Lemmatization.utility.helper import get_prefix_path
from Lemmatization.utility.helper import get_suffix_path
import csv


def get_suffixes():
    return read_file(get_suffix_path())


def get_prefixes():
    return read_file(get_prefix_path())


def read_file(filename):
    with open(filename, "r") as infile:
        data = infile.readlines()
    data = [x.strip() for x in data]
    return data


def read_csv(file_path):
    with open(file_path, 'r') as f:
        data = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    return data
