from pathlib import Path

from gendiff.diff_module.generate_diff import generate_diff

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


def test_generate_json_diff():
    """Testing json_diff module."""
    assert generate_diff(
        FIRST_FLAT_JSON,
        SECOND_FLAT_JSON,
    ) == COMPARE_FLAT_FILES
    assert generate_diff(
        FIRST_NESTED_JSON,
        SECOND_NESTED_JSON,
    ) == COMPARE_NESTED_FILES


def test_generate_yaml_diff():
    """Testing yaml_diff module."""
    assert generate_diff(
        FIRST_FLAT_YAML,
        SECOND_FLAT_YAML,
    ) == COMPARE_FLAT_FILES
    assert generate_diff(
        FIRST_NESTED_YAML,
        SECOND_NESTED_YAML,
    ) == COMPARE_NESTED_FILES


def test_files_extension():
    """Testing extension files match."""
    assert generate_diff(
        FIRST_FLAT_JSON,
        FIRST_FLAT_YAML,
    ) == 'Error! Files extension does not match!'
