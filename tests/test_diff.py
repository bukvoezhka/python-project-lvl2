from pathlib import Path

from gendiff.engine import generate_diff, make_ast_diff, prepare_files
from gendiff.formatters.plain import make_ast_plain_view as plain
from gendiff.formatters.stylish import make_ast_tree_view as stylish
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
FLAT_PLAIN_FORMAT = Path(
    FIXTURES_REPO, 'flat_plain_format.txt',
).read_text().replace(r'\n', '\n')
NESTED_PLAIN_FORMAT = Path(
    FIXTURES_REPO, 'nested_plain_format.txt',
).read_text().replace(r'\n', '\n')


def test_make_flat_ast():
    """Testing generate flat AST."""
    assert make_ast_diff(*prepare_files(
        FIRST_FLAT_JSON, SECOND_FLAT_JSON,
    )) == FLAT_AST
    assert make_ast_diff(*prepare_files(
        FIRST_FLAT_YAML, SECOND_FLAT_YAML,
    )) == FLAT_AST


def test_make_nested_ast():
    """Testing generate nested AST."""
    assert make_ast_diff(*prepare_files(
        FIRST_NESTED_JSON, SECOND_NESTED_JSON,
    )) == NESTED_AST
    assert make_ast_diff(*prepare_files(
        FIRST_NESTED_YAML, SECOND_NESTED_YAML,
    )) == NESTED_AST


def test_generate_flat_diff():
    """Testing flat diff module."""
    assert generate_diff(
        FIRST_FLAT_YAML, SECOND_FLAT_YAML,
    ) == COMPARE_FLAT_FILES
    assert generate_diff(
        FIRST_FLAT_JSON, SECOND_FLAT_JSON,
    ) == COMPARE_FLAT_FILES


def test_generate_nested_diff():
    """Testing nested diff module."""
    assert generate_diff(
        FIRST_NESTED_YAML, SECOND_NESTED_YAML,
    ) == COMPARE_NESTED_FILES
    assert generate_diff(
        FIRST_NESTED_JSON, SECOND_NESTED_JSON,
    ) == COMPARE_NESTED_FILES


def test_error_exceptions():
    """Testing extension files match."""
    assert isinstance(
        generate_diff(FIRST_FLAT_JSON, FIRST_FLAT_YAML),
        TypeError,
    )
    assert isinstance(
        generate_diff(FIRST_FLAT_JSON, FIRST_FLAT_YAML, 'random'),
        KeyError,
    )


def test_stylish_formatter():
    """Testing stylish formatter for AST."""
    assert stylish(FLAT_AST) == COMPARE_FLAT_FILES
    assert stylish(NESTED_AST) == COMPARE_NESTED_FILES
    assert generate_diff(
        FIRST_FLAT_JSON,
        SECOND_FLAT_JSON,
    ) == COMPARE_FLAT_FILES
    assert generate_diff(
        FIRST_NESTED_YAML,
        SECOND_NESTED_YAML,
    ) == COMPARE_NESTED_FILES


def test_plain_formatter():
    """Testing plain formatter for AST."""
    assert plain(FLAT_AST) == FLAT_PLAIN_FORMAT
    assert plain(NESTED_AST) == NESTED_PLAIN_FORMAT
    assert generate_diff(
        FIRST_FLAT_YAML,
        SECOND_FLAT_YAML,
        formatter='plain',
    ) == FLAT_PLAIN_FORMAT
    assert generate_diff(
        FIRST_NESTED_YAML,
        SECOND_NESTED_YAML,
        formatter='plain',
    ) == NESTED_PLAIN_FORMAT
