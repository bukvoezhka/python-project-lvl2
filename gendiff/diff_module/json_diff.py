import json
from collections import OrderedDict

JSON_DIFF_DICT = OrderedDict()


def generate_diff(json_file1, json_file2):
    """
    Create a dictionary of differences between JSON files.

    Args:
        json_file1: first JSON file,
        json_file2: second JSON file.

    Returns:
        dictionary of differences with comments.
    """
    json_dict1, json_dict2 = convert_json_to_dict(json_file1, json_file2)
    for key in sorted(set(json_dict1) | (set(json_dict2))):
        key_diff_status = check_key_statement(key, json_dict1, json_dict2)
        if key_diff_status == 'both':
            if json_dict1.get(key) == json_dict2.get(key):
                JSON_DIFF_DICT.update({
                    ('  {0}').format(key): json_dict1.get(key),
                })
            else:
                JSON_DIFF_DICT.update({
                    ('- {0}').format(key): json_dict1.get(key),
                    ('+ {0}').format(key): json_dict2.get(key),
                })
        if key_diff_status == 'first':
            JSON_DIFF_DICT.update({
                ('- {0}').format(key): json_dict1.get(key),
            })
        if key_diff_status == 'second':
            JSON_DIFF_DICT.update({
                ('+ {0}').format(key): json_dict2.get(key),
            })
    return json.dumps(JSON_DIFF_DICT, indent=2)


def check_key_statement(key, dict1, dict2):
    """
    Check statement of key in JSON dict.

    Args:
        key: key of dict to check,
        dict1: first JSON dict,
        dict2: second JSON dict.

    Returns:
        state of key in dict.
    """
    if key in dict1 and key in dict2:
        return 'both'
    if key in dict1 and key not in dict2:
        return 'first'
    if key not in dict1 and key in dict2:
        return 'second'


def convert_json_to_dict(json_file1, json_file2):
    """
    Format JSON file to python dict.

    Args:
        json_file1: first file,
        json_file2: second file.

    Returns:
        Tuples of converted object.
    """
    with open(json_file1) as file1:
        json_dict1 = json.load(file1)
    with open(json_file2) as file2:
        json_dict2 = json.load(file2)
    return json_dict1, json_dict2
