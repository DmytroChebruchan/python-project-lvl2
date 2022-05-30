#!/usr/bin/env python3
# changes boolin type to string with small first letter
import json
import yaml
from gendiff.parcer.parcer import format_parcer
from gendiff.additionals.replacers import none_to_null, bool_to_lower_case_str


def yml_reader(files_address):
    return yaml.safe_load(open(files_address))


def json_reader(files_address):
    return json.load(open(files_address))


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
                     none_to_null(bool_to_lower_case_str(dictionary)), pair))
    return pair


def transforms_dict_to_value(dictionary, level):
    result = '{'

    for key in dictionary:
        if not isinstance(dictionary[key], dict):
            exported_element = str(dictionary[key])
        else:
            exported_element = transforms_dict_to_value(dictionary[key],
                                                        level + 1)

        result = result + '\n' + '    ' * (level + 1) + key + ": "\
            + exported_element

    result = result + '\n' + '    ' * level + "}"

    return result


def transforms_option_to_string(key, level, value, operator='common'):
    operators = {"common": '    ',
                 "0": '  - ',
                 "1": '  + '}

    lower_case_bool = {"True": "true",
                       "False": "false",
                       "null": "null"}

    if isinstance(value, bool):
        value = lower_case_bool.get(str(value))

    if isinstance(value, dict):
        value = transforms_dict_to_value(value, level)

    result = '    ' * (level - 1) + operators.get(operator)\
        + str(key) + ": " + str(value) + '\n'
    return result
