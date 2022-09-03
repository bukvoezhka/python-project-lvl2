from pathlib import Path

from gendiff.diff_module.json_diff import generate_diff

first_file = Path('tests', 'fixtures', 'first_flat_file.json')
second_file = Path('tests', 'fixtures', 'second_flat_file.json')
json_compare = Path(
    'tests', 'fixtures', 'json_flat_compare.txt',
).read_text().replace(r'\n', '\n')


def test_generate_json_diff():
    """Testing json_diff module."""
    assert generate_diff(first_file, second_file) == json_compare
