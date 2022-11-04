from pathlib import Path

from gendiff.constants import AST_STRUCTURE, STATUS, FIlE_HANDLER
from gendiff.formatters.stylish import make_ast_tree_view as stylish


def convert_files(first_file, second_file, converter):
    """
    Convert input files to python dict.

    Args:
        first_file: first data file,
        second_file: second data file,
        converter: nessesary to convert function.

    Returns:
        Tuple of python dicts.
    """
    with open(first_file) as first:
        first_dict = converter(first)
    with open(second_file) as second:
        second_dict = converter(second)
    return first_dict, second_dict


def prepare_files(first_file, second_file):
    """
    Prepare input files for parsing.

    Args:
        first_file: first data file,
        second_file: second data file.

    Returns:
        Python dicts for parsing.

    Raises:
        ValueError: if files extension does not match.
    """
    for _, context in FIlE_HANDLER.items():
        if (Path(first_file).suffix in context['extns']):
            if (Path(second_file).suffix in context['extns']):
                return convert_files(
                    first_file, second_file, context['converter'],
                )
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


def check_value_status(key, node_values):
    """
    Check status of values.

    Args:
        key: current key from loop,
        node_values: values from two dict node.

    Returns:
        tuple with key, status and values for node.
    """
    first_value, second_value = node_values
    if first_value == second_value:
        return key, STATUS.equal, node_values
    if is_values_dict(first_value, second_value):
        return key, STATUS.children, node_values
    return key, STATUS.updated, node_values


def check_key_status(key, keys_sets, node_values):
    """
    Check status of keys.

    Args:
        key: current key from loop,
        keys_sets: keys from two dicts,
        node_values: values from two dict node.

    Returns:
        tuple with key, status and values for node.
    """
    first_keys, second_keys = keys_sets
    if key in first_keys - second_keys:
        return key, STATUS.deleted, node_values
    if key in second_keys - first_keys:
        return key, STATUS.added, node_values
    return check_value_status(key, node_values)


def make_ast_diff_node(key, key_status, node_values):
    """
    Make node for AST tree.

    Args:
        key: current key from loop,
        key_status: status of key for AST,
        node_values: tuple with value from dicts.

    Returns:
        dict node.
    """
    if key_status == STATUS.children:
        return AST_STRUCTURE[key_status](key, make_ast_diff(*node_values))
    return AST_STRUCTURE[key_status](key, node_values)


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
        diff.append(
            make_ast_diff_node(*check_key_status(
                key, (first_keys, second_keys),
                (first_dict.get(key), second_dict.get(key)),
            ),
            ))
    return diff


def generate_diff(first_file, second_file, formatter=stylish):
    """
    Create a view of differences between data interchage files.

    Args:
        first_file: first data file,
        second_file: second data file,
        formatter: default formatter for output view.

    Returns:
        view of differences with comments.
    """
    try:
        return formatter(make_ast_diff(*prepare_files(
            first_file, second_file,
        )))
    except ValueError:
        return ValueError('File extension does not match or is not supported.')
