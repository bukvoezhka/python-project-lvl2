from functools import partial
from json import dumps as make_ast_json_view
from pathlib import Path

from gendiff.constants import AST_STRUCTURE, FILE_HANDLER, SPACE_INDENT, STATUS
from gendiff.formatters.plain import make_ast_plain_view
from gendiff.formatters.stylish import make_ast_tree_view

FORMATTERS = {
    'json': partial(make_ast_json_view, indent=SPACE_INDENT),
    'plain': make_ast_plain_view,
    'stylish': make_ast_tree_view,
}


def convert_files(file, converter):
    """
    Convert input files to python dict.

    Args:
        file: data file,
        converter: nessesary to convert function.

    Returns:
        Tuple of python dicts.
    """
    with open(file) as convert_file:
        python_dict = converter(convert_file)
    return python_dict


def prepare_files(first_file, second_file):
    """
    Prepare input files for parsing.

    Args:
        first_file: first data file,
        second_file: second data file.

    Returns:
        Python dicts for parsing.
    """
    converted = []
    files = {
        first_file: Path(first_file).suffix,
        second_file: Path(second_file).suffix,
    }
    for file, extn in files.items():
        for _, context in FILE_HANDLER.items():
            if (extn in context['extns']):
                converted.append(convert_files(file, context['converter']))
                break
    return converted


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


def generate_diff(first_file, second_file, formatter='stylish'):
    """
    Create a view of differences between data interchage files.

    Args:
        first_file: first data file,
        second_file: second data file,
        formatter: formatter for customize output view.

    Returns:
        view of differences with comments.
    """
    try:
        return FORMATTERS[formatter](make_ast_diff(*prepare_files(
            first_file, second_file,
        )))
    except KeyError:
        return KeyError('Specified format is invalid.')
    except TypeError:
        return TypeError('Files extension is not supported.')
