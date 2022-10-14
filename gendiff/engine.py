import json
from pathlib import Path

import yaml
from gendiff.stylish import pretty_print_ast

FIlE_HANDLER = {
    'JSON': {
        'extns': ('.json'),
        'converter': json.load,
    },
    'YAML': {
        'extns': ('.yaml', '.yml'),
        'converter': yaml.safe_load,
    },
}
AST_KEY_STATUS = {
    'added': 'add',
    'deleted': 'del',
    'equal': 'eql',
    'updated': 'upd',
}


def prepare_files(first_file, second_file):
    """
    Prepare input files for parsing.

    Args:
        first_file: first data file,
        second_file: second data file.

    Returns:
        Dict of context for parsing.

    Raises:
        ValueError: if files extension does not match.
    """
    for _, context in FIlE_HANDLER.items():
        if (Path(first_file).suffix in context['extns']):
            if (Path(second_file).suffix in context['extns']):
                with open(first_file) as first:
                    first_dict = context['converter'](first)
                with open(second_file) as second:
                    second_dict = context['converter'](second)
                return first_dict, second_dict
    raise ValueError


def is_values_dict(first_value, second_value):
    """
    Cheking values for type.

    Args:
        first_value: first dict value,
        second_value: second dict value.

    Returns:
        boolean.
    """
    if isinstance(first_value, dict):
        if isinstance(second_value, dict):
            return True
    return False


def get_key_status(key, first, second):
    """
    Check status of key in to sets.

    Args:
        key: key from set,
        first: first set,
        second: second set.

    Returns:
        tuple with key ans staus.
    """
    if key in first - second:
        return key, AST_KEY_STATUS['deleted']
    if key in second - first:
        return key, AST_KEY_STATUS['added']
    return key, None


def make_ast_diff_node(key_info, first_value, second_value):
    """
    Make node for AST tree.

    Args:
        key_info: key with his diff status,
        first_value: first dict value,
        second_value: second dict value.

    Returns:
        dict node.
    """
    current_key, key_status = key_info
    if key_status == AST_KEY_STATUS['deleted']:
        return {
            'key': current_key,
            'value': first_value,
            'status': AST_KEY_STATUS['deleted'],
            'children': None,
        }
    if key_status == AST_KEY_STATUS['added']:
        return {
            'key': current_key,
            'value': second_value,
            'status': AST_KEY_STATUS['added'],
            'children': None,
        }
    if first_value == second_value:
        return {
            'key': current_key,
            'value': first_value,
            'status': AST_KEY_STATUS['equal'],
            'children': None,
        }
    return {
        'key': current_key,
        'value': {
            'old': first_value,
            'new': second_value,
        },
        'status': AST_KEY_STATUS['updated'],
        'children': None,
    }


def make_ast_diff(first_dict, second_dict):
    """
    Create a AST between two dicts.

    Args:
        first_dict: first dict,
        second_dict: second dict.

    Returns:
        list of dicts.
    """
    diff = []
    first_keys = set(first_dict)
    second_keys = set(second_dict)
    for key in sorted(first_keys | second_keys):
        first_value = first_dict.get(key)
        second_value = second_dict.get(key)
        if is_values_dict(first_value, second_value):
            diff.append({
                'key': key,
                'value': None,
                'status': AST_KEY_STATUS['updated'],
                'children': make_ast_diff(first_value, second_value),
            })
        else:
            diff.append(make_ast_diff_node(
                get_key_status(key, first_keys, second_keys),
                first_value,
                second_value,
            ))
    return diff


def generate_diff(first_file, second_file):
    """
    Create a view of differences between data interchage files.

    Args:
        first_file: first data file,
        second_file: second data file.

    Returns:
        view of differences with comments.
    """
    try:
        return pretty_print_ast(make_ast_diff(*prepare_files(
            first_file, second_file,
        )))
    except ValueError:
        return 'Error! Files extension does not match!'
