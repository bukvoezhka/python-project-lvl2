import json


def generate_diff(first_json_file, second_json_file):
    """
    Create a dictionary of differences between JSON files.

    Args:
        first_json_file: first JSON file,
        second_json_file: second JSON file.

    Returns:
        dictionary of differences with comments.
    """
    first_dict, second_dict = convert_json_to_dict(
        first_json_file, second_json_file,
    )
    dict_of_difference = build_diff_dictionary(first_dict, second_dict)
    output = json.dumps(dict_of_difference, indent=2, separators=('', ': '))
    return output.replace('"', '')


def build_diff_dictionary(first_dict, second_dict):
    """
    Create a dictionary of differences between JSON files.

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


def convert_json_to_dict(first_json_file, second_json_file):
    """
    Format JSON file to python dict.

    Args:
        first_json_file: first file,
        second_json_file: second file.

    Returns:
        Tuples of converted object.
    """
    with open(first_json_file) as first_file:
        first_dict = json.load(first_file)
    with open(second_json_file) as second_file:
        second_dict = json.load(second_file)
    return first_dict, second_dict
