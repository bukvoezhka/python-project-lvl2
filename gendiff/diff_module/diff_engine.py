def main(first_dict, second_dict):
    """
    Create a dictionary of differences between two dicts.

    Args:
        first_dict: first dict,
        second_dict: second dict.

    Returns:
        dictionary of differences.
    """
    diff_dict = {}
    first_file_keys = set(first_dict)
    second_file_keys = set(second_dict)
    for key in sorted(first_file_keys | second_file_keys):
        if key in first_file_keys - second_file_keys:
            diff_dict.update({('- {0}').format(key): first_dict.get(key)})
        elif key in second_file_keys - first_file_keys:
            diff_dict.update({('+ {0}').format(key): second_dict.get(key)})
        elif first_dict.get(key) == second_dict.get(key):
            diff_dict.update({('  {0}').format(key): first_dict.get(key)})
        else:
            diff_dict.update({
                ('- {0}').format(key): first_dict.get(key),
                ('+ {0}').format(key): second_dict.get(key),
            })
    return diff_dict
