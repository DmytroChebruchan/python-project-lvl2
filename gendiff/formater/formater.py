#!/usr/bin/env python3
from gendiff.additionals.additional_tools import transforms_option_to_string, \
    dict_to_complex_value, json_inner_parent_generator
from gendiff.additionals.checkers import is_deep
from gendiff.additionals.result_generators import plain_result_generator, \
    stylish_result_generator, json_result_appender
from gendiff.additionals.replacers import str_bool_to_lower


def stylish(dictionary):
    def inner(dictionary, result, level=1):
        for key in sorted(list(dictionary)):
            dict_value = dictionary[key]

            if isinstance(dict_value, dict) and is_deep(dict_value):
                value = inner(dict_value, "", level + 1)
                result = result + transforms_option_to_string(key, level,
                                                              value,
                                                              'common')

            elif isinstance(dict_value, list):
                result = stylish_result_generator(dict_value, key,
                                                  level, result)

            else:
                result = result + transforms_option_to_string(key, level,
                                                              dict_value,
                                                              'common')

        result = "{\n" + result + '    ' * (level - 1) + "}"
        return result
    return inner(dictionary, '')


def plain(dictionary):
    def inner(dictionary, result, parent):
        for key in sorted(list(dictionary)):
            if parent == '':
                inner_parent = key
            else:
                inner_parent = parent + "." + key

            added_line = ''
            if isinstance(dictionary[key], list):
                added_line = plain_result_generator(inner_parent,
                                                    dictionary[key])
            if isinstance(dictionary[key], dict):
                added_line = inner(dictionary[key], '', inner_parent)
            result = result + added_line

        return result
    return inner(dictionary, '', '')[1::]


def json_decoder(dictionary):
    result = {"added": {},
              "removed": {},
              "updated": {}}

    def inner(dictionary, result, parent):
        for key in dictionary:

            inner_parent = json_inner_parent_generator(parent, key)

            if isinstance(dictionary[key], dict):
                inner(dictionary[key], result, inner_parent)

            elif isinstance(dictionary[key], list):
                pair = list(map(dict_to_complex_value, dictionary[key]))
                result = json_result_appender(result, pair, key, inner_parent)

        result = str_bool_to_lower(result)
        return result

    return inner(dictionary, result, '')
