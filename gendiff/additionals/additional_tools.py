#!/usr/bin/env python3
# changes boolin type to string with small first letter
import json
import yaml
from gendiff.parcer.parcer import format_parcer


def bool_to_lower_case(dictionary):

    for key in dictionary:
        if dictionary[key] is False:
            dictionary[key] = 'false'
        elif dictionary[key] is True:
            dictionary[key] = 'true'
    return dictionary


def none_to_null(dictionary):
    result = {}
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            result = none_to_null(dictionary[key])
        else:
            if dictionary[key] is None:
                dictionary[key] = 'null'
    result = dictionary
    return result


def yml_reader(files_address):
    return yaml.safe_load(open(files_address))


def json_reader(files_address):
    return json.load(open(files_address))


def is_dict_deep(dictionary):
    for element in dictionary:
        if isinstance(dictionary[element], dict):
            return True
    return False


def common_pairs(first_dict, second_dict):
    result = {}
    for key in first_dict:
        if key in second_dict and first_dict[key] == second_dict[key]:
            result[key] = first_dict[key]
    return result


# reads files and terns them to dicts
def files_to_dict_reader(file_1, file_2):
    files = (file_1, file_2)

    format = format_parcer(file_1)

    formats = {'JSON': json_reader,
               'YML': yml_reader}

    pair = tuple(map(lambda file: dict(formats.get(format)(file)),
                     files))
    pair = tuple(map(lambda dictionary:
                     none_to_null(bool_to_lower_case(dictionary)), pair))
    return pair
