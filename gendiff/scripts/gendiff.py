#!/usr/bin/env python3
import json
import yaml
from gendiff.scripts.parcer import parcer
from gendiff.formater.decoder import stylish, plain


# changes boolin type to string with small first letter
def replace_F_T_to_f_t(first_dict):

    for key in first_dict:
        if first_dict[key] is False:
            first_dict[key] = 'false'
        elif first_dict[key] is True:
            first_dict[key] = 'true'

    return first_dict


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


# finder of format
def format_parcer(first_file):
    found_format = ''

    i = 0
    while i < len(first_file):
        if first_file[i] == '.':
            break
        i = i + 1
    found_format = str(first_file[i + 1:]).upper()

    formats = {'JSON': 'JSON',
               'YAML': 'YML',
               'YML': 'YML'}

    return formats.get(found_format)


def yml_reader(files_address):
    return yaml.safe_load(open(files_address))


def json_reader(files_address):
    return json.load(open(files_address))


# reads files and terns them to dicts
def files_to_dict_reader(file_1, file_2):

    dict_1 = {}
    dict_2 = {}

    format = format_parcer(file_1)

    formats = {'JSON': json_reader,
               'YML': yml_reader}

    pair = list(map(lambda file: dict(formats.get(format)(file)),
                    [file_1, file_2]))
    dict_1, dict_2 = pair

    dict_1 = none_null(replace_F_T_to_f_t(dict_1))
    dict_2 = none_null(replace_F_T_to_f_t(dict_2))

    return dict_1, dict_2


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
                pair_values = first_dict[key], second_dict[key]
                if isinstance(first_dict.get(key), dict) \
                        and isinstance(second_dict.get(key), dict):
                    diff_dict[key] = diff_dict_generator(*pair_values)
                else:
                    if pair_values[0] != pair_values[1]:
                        diff_dict[key] = [*pair_values]
                    else:
                        diff_dict[key] = first_dict[key]
        else:
            # generating dictionaries with differences
            same_keys_diff_values = generator_same_keys_diff_values(first_dict,
                                                                    second_dict)
            diff_dict = diff_dict | same_keys_diff_values

        return diff_dict
    return inner(first_dict, second_dict, {})


def inner_dict(dictionary):
    return list(filter(lambda x: isinstance(dictionary[x], dict), dictionary))


def generate_diff(first_files_address, second_files_address, format='stylish'):
    if format is None:
        format = 'stylish'

    first_dict, second_dict = files_to_dict_reader(first_files_address,
                                                   second_files_address)

    result = []
    diff_dict = diff_dict_generator(first_dict, second_dict)

    decoders = {'stylish': stylish,
                'plain': plain}

    result = decoders.get(format)(diff_dict)

    return result


def main():
    parce = parcer()
    result = generate_diff(parce[0], parce[1], parce[2])
    return result


if __name__ == '__main__':
    main()
