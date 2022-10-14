#!/usr/bin/env python3
"""Gendiff module description."""
import argparse

from gendiff.engine import generate_diff
from gendiff.stylish import pretty_print_ast


def main():
    """Output description for CLI."""
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.',
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    print(generate_diff(
        first_file=args.first_file,
        second_file=args.second_file,
        formatter=pretty_print_ast,
    ))


if __name__ == '__main__':
    main()
