#!/usr/bin/env python3


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


def bool_to_lower_case_str(dictionary):

    for key in dictionary:
        if dictionary[key] is False:
            dictionary[key] = 'false'
        elif dictionary[key] is True:
            dictionary[key] = 'true'
    return dictionary


def str_bool_to_lower(result):
    result = str(result).replace("'", "\"")
    result = result.replace("True", "true").replace("False", "false")
    return result
