import json
from pathlib import Path

import yaml
from gendiff.diff_module.diff_engine import main


def convert_files(first_file, second_file, converter):
    """
    Convert files to python dict.

    Args:
        first_file: first interchange file,
        second_file: second interchange file,
        converter: function for convert file.

    Returns:
        Tuples of converted object.
    """
    with open(first_file) as first:
        first_dict = converter(first)
    with open(second_file) as second:
        second_dict = converter(second)
    return first_dict, second_dict


FIlE_HANDLER = {
    'JSON': {
        'exts': ('.json'),
        'converter': json.load,
    },
    'YAML': {
        'exts': ('.yaml', '.yml'),
        'converter': yaml.safe_load,
    },
}


def generate_diff(first_file, second_file):
    """
    Create a view of differences between data interchage files.

    Args:
        first_file: first data file,
        second_file: second data file.

    Returns:
        view of differences with comments.
    """
    context = cheking_files_type(
        first_file, second_file,
    )
    if context:
        first_dict, second_dict = convert_files(
            first_file, second_file, context.get('converter'),
        )
        dict_of_difference = main(first_dict, second_dict)
        pretty_print_dict = json.dumps(
            dict_of_difference, indent=2, separators=('', ': '),
        )
        return pretty_print_dict.replace('"', '')
    return 'Error! Files extension does not match!'


def cheking_files_type(first_file, second_file):
    """
    Cheking file extension of input files.

    Args:
        first_file: first data file,
        second_file: second data file.

    Returns:
        Dict of context for parsing.
    """
    first_ext = Path(first_file).suffix
    second_ext = Path(second_file).suffix
    for _, context in FIlE_HANDLER.items():
        extensions = context.get('exts')
        if (first_ext in extensions) and (second_ext in extensions):
            return context
