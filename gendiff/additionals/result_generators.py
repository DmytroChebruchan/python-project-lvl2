#!/usr/bin/env python3
from gendiff.additionals.additional_tools import transforms_option_to_string, \
    dict_to_complex_value, index_of_None_founder
from gendiff.additionals.replacers import replaces_of_special_values


def plain_result_generator(key, list_of_values):

    # updating pair by replacing dicts with '[complex value]'
    pair = list(map(dict_to_complex_value, list_of_values))

    # updating pair by replacing bool and None elements
    pair = list(map(replaces_of_special_values, pair))

    # preparations of templates
    added_element = ('added with value: {}').format(pair[1])
    updated_element = ('updated. From {} to {}').format(*pair)

    # finding index of None element
    index = index_of_None_founder(list_of_values)

    action_dict = {'1': 'removed',
                   '0': added_element,
                   '2': updated_element}

    action = action_dict.get(str(index))
    result = '\nProperty \'{}\' was {}'.format(key, action)

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


def json_result_appender(result, pair, key, inner_parent):
    removed_element, added_element = pair

    if removed_element is None:
        result['added'][inner_parent] = added_element
    else:
        result['removed'][str(key)] = removed_element

    return result
