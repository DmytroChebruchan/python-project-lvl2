#!/usr/bin/env python3
from gendiff.additionals.additional_tools import transforms_option_to_string


def plain_result_generator(key, list_of_values):

    # updating pair by replacing dicts with '[complex value]'
    pair = list(map(lambda val:
                    '[complex value]' if isinstance(val, dict) else val,
                    list_of_values))

    # updating pair by replacing bool and None elements
    bool_elements = {'True': 'true',
                     'False': 'false',
                     'null': 'null',
                     'None': 'None',
                     '[complex value]': '[complex value]',
                     '0': '0'}
    pair = list(map(lambda val:
                    bool_elements.get(str(val))
                    if str(val) in bool_elements else str("'{}'".format(val)),
                    pair))

    # preparations of templates
    template = '\nProperty \'{}\' was {}'
    added_element = ('added with value: {}').format(pair[1])
    updated_element = ('updated. From {} to {}').format(*pair)

    # finding index of None element
    index = 2
    for i in [0, 1]:
        if list_of_values[i] is None:
            index = i
            break

    action_dict = {'1': 'removed',
                   '0': added_element,
                   '2': updated_element}

    action = action_dict.get(str(index))
    result = template.format(key, action)

    return result


def stylish_result_generator(pair, key, level, result):
    first_element, second_element = pair
    if first_element is None:
        result = result + transforms_option_to_string(key, level,
                                                      second_element,
                                                      str(1))
    elif second_element is None:
        result = result + transforms_option_to_string(key, level,
                                                      first_element, str(0))
    else:
        result = result + transforms_option_to_string(key, level,
                                                      first_element,
                                                      str(0))
        result = result + transforms_option_to_string(key, level,
                                                      second_element,
                                                      str(1))
    return result
