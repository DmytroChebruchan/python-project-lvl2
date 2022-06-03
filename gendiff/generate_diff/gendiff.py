#!/usr/bin/env python3
from gendiff.formater.formater import stylish, plain, json_decoder
from gendiff.additionals.additional_tools import files_to_dict_reader
from gendiff.dictionaries.generator import diff_dict_generator


def generate_diff(first_files_address, second_files_address, format='stylish'):
    if format is None:
        format = 'stylish'

    first_dict, second_dict = files_to_dict_reader(first_files_address,
                                                   second_files_address)

    result = []
    diff_dict = diff_dict_generator([first_dict, second_dict])

    decoders = {'stylish': stylish,
                'plain': plain,
                'json': json_decoder}

    result = decoders.get(format)(diff_dict)
    print(result)

    return result
