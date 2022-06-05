def generator_of_diff_dict_diff_key(first_dict, second_dict):
    unique_pairs = {}

    unique_keys = set(first_dict) - set(second_dict)
    for key in unique_keys:
        unique_pairs[key] = [first_dict[key], None]

    unique_keys = set(second_dict) - set(first_dict)
    for key in unique_keys:
        unique_pairs[key] = [None, second_dict[key]]

    return unique_pairs


def diff_dict_composer(first_dict, second_dict, diff_dict):
    same_keys_and_same_values = common_pairs(first_dict, second_dict)
    unique_pairs = generator_of_diff_dict_diff_key(first_dict, second_dict)

    return diff_dict | same_keys_and_same_values | unique_pairs


def common_pairs(first_dict, second_dict):
    result = {}
    for key in first_dict:
        if key in second_dict and first_dict[key] == second_dict[key]:
            result[key] = first_dict[key]
    return result
