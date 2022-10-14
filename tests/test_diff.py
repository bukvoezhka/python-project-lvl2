from pathlib import Path

from gendiff.engine import generate_diff, make_ast_diff, prepare_files
from gendiff.stylish import pretty_print_ast
from tests.fixtures.flat_ast import FLAT_AST
from tests.fixtures.nested_ast import NESTED_AST

FIXTURES_REPO = Path('tests', 'fixtures')

FIRST_FLAT_JSON = Path(FIXTURES_REPO, 'flat_file1.json')
SECOND_FLAT_JSON = Path(FIXTURES_REPO, 'flat_file2.json')
FIRST_NESTED_JSON = Path(FIXTURES_REPO, 'nested_file1.json')
SECOND_NESTED_JSON = Path(FIXTURES_REPO, 'nested_file2.json')

FIRST_FLAT_YAML = Path(FIXTURES_REPO, 'flat_file1.yml')
SECOND_FLAT_YAML = Path(FIXTURES_REPO, 'flat_file2.yml')
FIRST_NESTED_YAML = Path(FIXTURES_REPO, 'nested_file1.yml')
SECOND_NESTED_YAML = Path(FIXTURES_REPO, 'nested_file2.yml')

COMPARE_FLAT_FILES = Path(
    FIXTURES_REPO, 'compare_flat_files.txt',
).read_text().replace(r'\n', '\n')
COMPARE_NESTED_FILES = Path(
    FIXTURES_REPO, 'compare_nested_files.txt',
).read_text().replace(r'\n', '\n')


def test_flat_diff():
    """Testing flat diff module."""
    assert generate_diff(
        FIRST_FLAT_YAML, SECOND_FLAT_YAML,
    ) == COMPARE_FLAT_FILES
    assert generate_diff(
        FIRST_FLAT_JSON, SECOND_FLAT_JSON,
    ) == COMPARE_FLAT_FILES


def test_nested_diff():
    """Testing nested diff module."""
    assert generate_diff(
        FIRST_NESTED_YAML, SECOND_NESTED_YAML,
    ) == COMPARE_NESTED_FILES
    assert generate_diff(
        FIRST_NESTED_JSON, SECOND_NESTED_JSON,
    ) == COMPARE_NESTED_FILES


def test_match_files_extension():
    """Testing extension files match."""
    assert generate_diff(
        FIRST_FLAT_JSON, FIRST_FLAT_YAML,
    ) == 'Error! Files extension does not match!'


def test_make_flat_ast():
    """Testing flat AST."""
    assert make_ast_diff(*prepare_files(
        FIRST_FLAT_JSON, SECOND_FLAT_JSON,
    )) == FLAT_AST
    assert make_ast_diff(*prepare_files(
        FIRST_FLAT_YAML, SECOND_FLAT_YAML,
    )) == FLAT_AST


def test_make_nested_ast():
    """Testing nested AST."""
    assert make_ast_diff(*prepare_files(
        FIRST_NESTED_JSON, SECOND_NESTED_JSON,
    )) == NESTED_AST
    assert make_ast_diff(*prepare_files(
        FIRST_NESTED_YAML, SECOND_NESTED_YAML,
    )) == NESTED_AST


def test_pretty_print_flat_ast():
    """Testing stylish print of AST."""
    assert pretty_print_ast(FLAT_AST) == COMPARE_FLAT_FILES


def test_pretty_print_nested_ast():
    """Testing stylish print of AST."""
    assert pretty_print_ast(NESTED_AST) == COMPARE_NESTED_FILES
