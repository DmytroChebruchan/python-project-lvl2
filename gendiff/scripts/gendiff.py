#!/usr/bin/env python3

import argparse
import json

parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')
parser.add_argument('-f', '--format',
                    help='set format of output')
args = parser.parse_args()


def generate_diff():

    first_dict = dict(json.load(open('file1.json')))
    second_dict = dict(json.load(open('file2.json')))

    merged_unique_keys_list = sorted(first_dict | second_dict)
    merged_dict = {}
    merged_list = []
    result = '{ \n'

    # replacing False and True to false and true as string
    for key in first_dict:
        if first_dict[key] is False:
            first_dict[key] = 'false'
        elif first_dict[key] is True:
            first_dict[key] = 'true'

    for key in second_dict:
        if second_dict[key] is False:
            second_dict[key] = 'false'
        elif second_dict[key] is True:
            second_dict[key] = 'true'

    # creating merged dict
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

    # creating merged incripted list with all information
    for key in merged_dict:
        merged_list.append([key, merged_dict[key]])

    merged_list.sort()

    # generating string from incripted list
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
    print(result)

    return result


def main():
    generate_diff()


if __name__ == '__main__':
    main()
