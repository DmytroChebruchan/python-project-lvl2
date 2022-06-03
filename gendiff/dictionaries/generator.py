#!/usr/bin/env python3
from gendiff.additionals.additional_tools import diff_dict_composer
from gendiff.additionals.checkers import is_dict_deep


def generator_same_keys_diff_values(first_dict, second_dict):

    first_set = set(first_dict)
    second_set = set(second_dict)
    mutual_keys = first_set & second_set
    mutual_keys_unique_value = set(filter(lambda x:
                                          first_dict[x] != second_dict[x],
                                          mutual_keys))

    result = {}
    for key in mutual_keys_unique_value:
        result[key] = [first_dict[key], second_dict[key]]
    return result


def sub_dict_filler(pair_values, diff_dict, key, value):
    if pair_values[0] != pair_values[1]:
        diff_dict[key] = [*pair_values]
    else:
        diff_dict[key] = value
    return diff_dict


def filler_of_diff_dict_with_common(common_keys, diff_dict,
                                    first_dict, second_dict):
    for key in common_keys:
        pair_values = first_dict[key], second_dict[key]

        if isinstance(first_dict.get(key), dict) \
                and isinstance(second_dict.get(key), dict):
            diff_dict[key] = diff_dict_generator(pair_values)
        else:
            diff_dict = sub_dict_filler(pair_values, diff_dict,
                                        key, first_dict[key])

    return diff_dict


def diff_dict_generator(pair):
    first_dict, second_dict = pair

    def inner(first_dict, second_dict, diff_dict):

        diff_dict = diff_dict_composer(first_dict, second_dict, diff_dict)

        # for deep dictionaries
        if all((is_dict_deep(first_dict), is_dict_deep(second_dict))):
            common_keys = set(first_dict) & set(second_dict)
            diff_dict = filler_of_diff_dict_with_common(common_keys, diff_dict,
                                                        first_dict, second_dict)
        else:
            # generating dictionaries with differences
            same_keys_diff_values = generator_same_keys_diff_values(first_dict,
                                                                    second_dict)
            diff_dict = diff_dict | same_keys_diff_values

        return diff_dict
    return inner(first_dict, second_dict, {})
