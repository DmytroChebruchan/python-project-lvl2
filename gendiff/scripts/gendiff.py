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


def merged_unique_keys_list_generator(first_dict, second_dict):
    return sorted(first_dict | second_dict)


def decoder_of_lines_with_same_value(key, value, level):
    return '    ' * level + str(key) + ": " + str(value)


def decoder_of_lines_with_diff_value(key, value, level):
    result = ''
    argument = 0
    operator = ''
    if value[0] is None or value[1] is None:
        if value[0] is None:
            operator = '-'
            argument = 1
        if value[1] is None:
            operator = '+'
        result = '  ' * level + operator + ' ' + str(key)
        + ": " + str(value[argument])
    else:
        result = ' +  ' + str(key) + ": " + str(value[0])
        result = result + '\n -  ' + str(key) + ": " + str(value[1])
    return result


def decoder(diction):
    result = ''
    level = 1
    children = []

    def inner(diction):
        print(diction)
        result = "\n{" + '    ' * level
        for key in diction:
            if isinstance(diction[key], dict) is False:
                if isinstance(diction[key], list) is False:
                    result = result + "\n" \
                        + decoder_of_lines_with_same_value(key,
                                                           diction[key],
                                                           level)
                else:
                    result = result + "\n" \
                        + decoder_of_lines_with_diff_value(key,
                                                           diction[key],
                                                           level)
            else:
                children.append(diction[key])
        if children == []:
            result = result + '    ' * (level - 1) + "\n}"
        print("inner result is " + str(result))
        return result

    result = inner(diction)

    print("result is " + str(result))
    print("children are " + str(children))
    for child in children:
        inner(child)
    return result


def generate_diff(first_files_address, second_files_address, format=None):
    first_dict, second_dict = files_to_dict_reader(first_files_address,
                                                   second_files_address,
                                                   format)
    result = []

    diff_dict = {}
    list_sub_dict = []

    def inner(first_dict, second_dict, diff_dict):
        for key in first_dict:
            if type(first_dict[key]) is not dict:
                if key in second_dict:
                    if first_dict[key] == second_dict[key]:
                        diff_dict[key] = first_dict[key]
                    else:
                        diff_dict[key] = [first_dict[key], second_dict[key]]
                else:
                    diff_dict[key] = [first_dict[key], None]
            else:
                if key in second_dict:
                    if type(second_dict[key]) is dict:
                        list_sub_dict.append([key, [first_dict[key],
                                                    second_dict[key]]])
                    else:
                        diff_dict[key] = [first_dict[key], second_dict[key]]
                else:
                    diff_dict[key] = [first_dict[key], None]

        for key in second_dict:
            if type(second_dict[key]) is not dict:
                if key not in first_dict:
                    diff_dict[key] = [None, second_dict[key]]
            else:
                if key not in first_dict:
                    diff_dict[key] = [None, second_dict[key]]

    inner(first_dict, second_dict, diff_dict)

    def pre_inner(set_of_dicts):
        diff_dict[set_of_dicts[0]] = {}
        inner(set_of_dicts[1][0], set_of_dicts[1][1],
              diff_dict[set_of_dicts[0]])

    list(map(pre_inner, list_sub_dict))
    result = decoder(diff_dict)

    return result


def main():
    parce = parcer()
    result = generate_diff(parce[0], parce[1], parce[2])
    return result


if __name__ == '__main__':
    main()
