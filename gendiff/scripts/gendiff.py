#!/usr/bin/env python3
import json
import yaml
from gendiff.scripts.parcer import parcer


# changes boolin type to string with small first letter
def replace_F_T_to_f_t(first_dict):

    for key in first_dict:
        if first_dict[key] is False:
            first_dict[key] = 'false'
        elif first_dict[key] is True:
            first_dict[key] = 'true'

    return first_dict


# changer of dict to sorted list for further decoding
def dict_to_sorted_list(dictionary):
    result = []

    for key in dictionary:
        result.append([key, dictionary[key]])
    result.sort()

    return result


# finder of format
def format_parcer(first_file, format):
    result = ''
    found_format = ''

    if format is None:
        i = 0
        while i < len(first_file):
            if first_file[i] == '.':
                break
            i = i + 1
        found_format = str(first_file[i + 1:])
    else:
        found_format = format

    found_format = found_format.upper()

    if found_format == 'JSON':
        result = 'JSON'
    if found_format == 'YAML' or found_format == 'YML':
        result = 'YML'

    return result


def yml_reader(files_address):
    return yaml.safe_load(open(files_address))


def json_reader(files_address):
    return json.load(open(files_address))


def none_null(dictionary):
    result = {}
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            result = none_null(dictionary[key])
        else:
            if dictionary[key] is None:
                dictionary[key] = 'null'
    result = dictionary
    return result


# reads files and terns them to dicts
def files_to_dict_reader(first_file, second_file, format):

    first_dict = {}
    second_dict = {}

    format = format_parcer(first_file, format)

    if format == 'JSON':
        first_dict = dict(json_reader(first_file))
        second_dict = dict(json_reader(second_file))

    if format == 'YML':
        first_dict = dict(yml_reader(first_file))
        second_dict = dict(yml_reader(second_file))

    first_dict = none_null(replace_F_T_to_f_t(first_dict))
    second_dict = none_null(replace_F_T_to_f_t(second_dict))

    return first_dict, second_dict


def generator_same_keys_diff_values(first_dict, second_dict):

    first_set = set(first_dict)
    second_set = set(second_dict)
    mutual_keys = first_set & second_set
    mutual_keys_unique_value = set(filter(lambda x:
                                          first_dict[x] != second_dict[x],
                                          mutual_keys))

    result = {}
    for key in mutual_keys_unique_value:
        result[key] = [first_dict[key], second_dict[key]]
    return result


def generator_of_diff_dict_diff_key(first_dict, second_dict):
    unique_pairs = {}
    for key in first_dict:
        if key not in second_dict:
            unique_pairs[key] = [first_dict[key], None]
    for key in second_dict:
        if key not in first_dict:
            unique_pairs[key] = [None, second_dict[key]]
    return unique_pairs


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


def diff_dict_generator(first_dict, second_dict):
    def inner(first_dict, second_dict, diff_dict):

        same_keys_and_same_values = common_pairs(first_dict, second_dict)
        unique_pairs = generator_of_diff_dict_diff_key(first_dict, second_dict)
        diff_dict = diff_dict | same_keys_and_same_values | unique_pairs

        # for deep dictionaries
        if is_dict_deep(first_dict) and is_dict_deep(second_dict):
            common_keys = set(first_dict) & set(second_dict)
            for key in common_keys:
                if isinstance(first_dict.get(key), dict) \
                        and isinstance(second_dict.get(key), dict):
                    diff_dict[key] = diff_dict_generator(first_dict[key],
                                                         second_dict[key])
                else:
                    if first_dict[key] != second_dict[key]:
                        diff_dict[key] = [first_dict[key], second_dict[key]]
                    else:
                        diff_dict[key] = first_dict[key]
        else:
            # generating dictionaries with differences
            same_keys_diff_values = generator_same_keys_diff_values(first_dict,
                                                                    second_dict)
            diff_dict = diff_dict | same_keys_diff_values

        return diff_dict
    return inner(first_dict, second_dict, {})


def dict_value(dictionary, level):
    result = '{'
    for key in dictionary:
        if not isinstance(dictionary[key], dict):
            exported_element = str(dictionary[key])
        else:
            exported_element = dict_value(dictionary[key], level + 1)

        result = result + '\n' + '    ' * (level + 1) + key + ": "\
            + exported_element

    result = result + '\n' + '    ' * level + "}"

    return result


def to_string(key, level, value, operator='common'):
    operators = {"common": '    ',
                 "0": '  - ',
                 "1": '  + '}

    lower_case_bool = {"True": "true",
                       "False": "false",
                       "null": "null"}
    if isinstance(value, bool):
        value = lower_case_bool.get(str(value))

    if isinstance(value, dict):
        value = dict_value(value, level)

    result = '    ' * (level - 1) + operators.get(operator)\
        + str(key) + ": " + str(value) + '\n'
    return result


def dict_or_list_checker(element, node):
    if isinstance(node[element], dict) or isinstance(node[element], list):
        return element
    else:
        return False


def is_deep(node):
    keys_dicts = list(filter(lambda x: dict_or_list_checker(x, node), node))
    return True if keys_dicts else False


def inner_dict(dictionary):
    return list(filter(lambda x: isinstance(dictionary[x], dict), dictionary))


def result_generator(pair, key, level, result):
    first_element, second_element = pair
    if first_element is None:
        result = result + to_string(key, level,
                                    second_element, str(1))
    elif second_element is None:
        result = result + to_string(key, level,
                                    first_element, str(0))
    else:
        result = result + to_string(key, level,
                                    first_element,
                                    str(0))
        result = result + to_string(key, level,
                                    second_element,
                                    str(1))
    return result


def stylish(dictionary):
    def inner(dictionary, result, level=1):
        for key in sorted(list(dictionary)):
            if isinstance(dictionary[key], dict) and is_deep(dictionary[key]):
                value = inner(dictionary[key], "", level + 1)
                result = result + to_string(key, level,
                                            value, 'common')
            elif isinstance(dictionary[key], list):
                result = result_generator(dictionary[key], key, level, result)
            else:
                result = result + to_string(key, level,
                                            dictionary[key], 'common')
        result = "{\n" + result + '    ' * (level - 1) + "}"
        return result
    return str('\n' + inner(dictionary, ''))


def generate_diff(first_files_address, second_files_address, format=None):
    first_dict, second_dict = files_to_dict_reader(first_files_address,
                                                   second_files_address,
                                                   format)
    result = []
    diff_dict = diff_dict_generator(first_dict, second_dict)

    result = stylish(diff_dict)
    return result


def main():
    parce = parcer()
    result = generate_diff(parce[0], parce[1], parce[2])
    return result


if __name__ == '__main__':
    main()
