#!/usr/bin/env python3


def is_dict_deep(dictionary):
    for element in dictionary:
        if isinstance(dictionary[element], dict):
            return True
    return False


def is_dict_or_list(element, node):
    return isinstance(node[element], dict) or isinstance(node[element], list)


def is_deep(node):
    keys_dicts = list(filter(lambda x: is_dict_or_list(x, node), node))
    return True if keys_dicts else False
