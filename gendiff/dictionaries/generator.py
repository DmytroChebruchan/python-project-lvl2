#!/usr/bin/env python3
from gendiff.additionals.additional_tools import is_dict_deep, common_pairs


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


def generator_of_diff_dict_diff_key(first_dict, second_dict):
    unique_pairs = {}
    for key in first_dict:
        if key not in second_dict:
            unique_pairs[key] = [first_dict[key], None]
    for key in second_dict:
        if key not in first_dict:
            unique_pairs[key] = [None, second_dict[key]]
    return unique_pairs


def diff_dict_generator(first_dict, second_dict):
    def inner(first_dict, second_dict, diff_dict):

        same_keys_and_same_values = common_pairs(first_dict, second_dict)
        unique_pairs = generator_of_diff_dict_diff_key(first_dict, second_dict)
        diff_dict = diff_dict | same_keys_and_same_values | unique_pairs

        # for deep dictionaries
        if all((is_dict_deep(first_dict), is_dict_deep(second_dict))):
            common_keys = set(first_dict) & set(second_dict)

            for key in common_keys:
                pair_values = first_dict[key], second_dict[key]
                if isinstance(first_dict.get(key), dict) \
                        and isinstance(second_dict.get(key), dict):
                    diff_dict[key] = diff_dict_generator(*pair_values)
                else:
                    if pair_values[0] != pair_values[1]:
                        diff_dict[key] = [*pair_values]
                    else:
                        diff_dict[key] = first_dict[key]
        else:
            # generating dictionaries with differences
            same_keys_diff_values = generator_same_keys_diff_values(first_dict,
                                                                    second_dict)
            diff_dict = diff_dict | same_keys_diff_values

        return diff_dict
    return inner(first_dict, second_dict, {})