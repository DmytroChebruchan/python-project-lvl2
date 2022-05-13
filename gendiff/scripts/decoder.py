#!/usr/bin/env python3
def is_deep(node):
    keys_dicts = list(filter(lambda x: dict_or_list_checker(x, node), node))
    return True if keys_dicts else False


def dict_or_list_checker(element, node):
    if isinstance(node[element], dict) or isinstance(node[element], list):
        return element
    else:
        return False


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
