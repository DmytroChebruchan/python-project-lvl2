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


# merger of dicts saving source of keys and their values
def dict_merger(merged_unique_keys_list, first_dict, second_dict):
    merged_dict = {}

    for key in merged_unique_keys_list:
        if key in first_dict and key in second_dict:
            if first_dict[key] == second_dict[key]:
                merged_dict[key] = [first_dict[key]]
            else:
                merged_dict[key] = [first_dict[key], second_dict[key]]
        elif key in first_dict:
            merged_dict[key] = [first_dict[key], None]
        else:
            merged_dict[key] = [None, second_dict[key]]

    return merged_dict


# changer of dict to sorted list for further decoding
def dict_to_sorted_list(dictionary):
    result = []

    for key in dictionary:
        result.append([key, dictionary[key]])
    result.sort()

    return result


# decoder of complex list to required string format
def result_generator(merged_list):
    result = '\n{ \n'

    for element in merged_list:
        if len(element[1]) == 1:
            result = result + '    "'\
                + str(element[0]) + '": ' + str(element[1][0]) + '\n'
        elif element[1][0] is None:
            result = result + '  + "'\
                + str(element[0]) + '": ' + str(element[1][1]) + '\n'
        elif element[1][1] is None:
            result = result + '  - "'\
                + str(element[0]) + '": ' + str(element[1][0]) + '\n'
        else:
            result = result + '  - "'\
                + str(element[0]) + '": ' + str(element[1][0]) + '\n'
            result = result + '  + "'\
                + str(element[0]) + '": ' + str(element[1][1]) + '\n'

    result = result + "}"
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

    return first_dict, second_dict


# generates differences
def generate_diff(first_files_address, second_files_address, format=None):

    # reading files and converting them to dicts
    first_dict, second_dict = files_to_dict_reader(first_files_address,
                                                   second_files_address,
                                                   format)

    merged_unique_keys_list = sorted(first_dict | second_dict)
    print('\nmerged_unique_keys_list is ' + str(merged_unique_keys_list) + '\n')
    merged_dict = {}
    merged_list = []

    # replacing False and True to false and true as string
    first_dict = replace_F_T_to_f_t(first_dict)
    second_dict = replace_F_T_to_f_t(second_dict)

    # creating merged dict
    merged_dict = dict_merger(merged_unique_keys_list, first_dict, second_dict)

    # creating merged incripted list with all information
    merged_list = dict_to_sorted_list(merged_dict)

    # decoded result
    result = result_generator(merged_list)

    return result


def main():
    parce = parcer()
    result = generate_diff(parce[0], parce[1], parce[2])
    return result


if __name__ == '__main__':
    main()
