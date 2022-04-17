#!/usr/bin/env python3

import json
from parcer import parcer


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
    result = '{ \n'

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


def generate_diff(first_file, second_file):

    first_dict = dict(json.load(open(first_file)))
    second_dict = dict(json.load(open(second_file)))

    merged_unique_keys_list = sorted(first_dict | second_dict)

    merged_dict = {}
    merged_list = []
    result = '{ \n'

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
    generate_diff(parce[0], parce[1])


if __name__ == '__main__':
    main()
