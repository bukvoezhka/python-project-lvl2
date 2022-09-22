from pathlib import Path

from gendiff.diff_module.generate_diff import generate_diff

FIXTURES_REPO = Path('tests', 'fixtures')

FIRST_FLAT_JSON = Path(FIXTURES_REPO, 'first_flat_file.json')
SECOND_FLAT_JSON = Path(FIXTURES_REPO, 'second_flat_file.json')

FIRST_FLAT_YAML = Path(FIXTURES_REPO, 'first_flat_file.yml')
SECOND_FLAT_YAML = Path(FIXTURES_REPO, 'second_flat_file.yml')

COMPARE_FLAT_FILES = Path(
    FIXTURES_REPO, 'compare_flat_files.txt',
).read_text().replace(r'\n', '\n')


def test_generate_json_diff():
    """Testing json_diff module."""
    assert generate_diff(
        FIRST_FLAT_JSON,
        SECOND_FLAT_JSON,
    ) == COMPARE_FLAT_FILES


def test_generate_yaml_diff():
    """Testing yaml_diff module."""
    assert generate_diff(
        FIRST_FLAT_YAML,
        SECOND_FLAT_YAML,
    ) == COMPARE_FLAT_FILES


def test_files_extension():
    """Testing extension files match."""
    assert generate_diff(
        FIRST_FLAT_JSON,
        FIRST_FLAT_YAML,
    ) == 'Error! Files extension does not match!'
