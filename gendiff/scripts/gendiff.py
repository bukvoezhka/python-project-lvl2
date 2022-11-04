#!/usr/bin/env python3
"""Gendiff module description."""
import argparse

from gendiff.engine import generate_diff
from gendiff.formatters.plain import make_ast_plain_view
from gendiff.formatters.stylish import make_ast_tree_view

FORMATTERS = {
    None: make_ast_tree_view,
    'plain': make_ast_plain_view,
}


def main():
    """Output description for CLI."""
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.',
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    try:
        print(generate_diff(
            first_file=args.first_file,
            second_file=args.second_file,
            formatter=FORMATTERS[args.format],
        ))
    except KeyError:
        print('The specified format is invalid.')


if __name__ == '__main__':
    main()
