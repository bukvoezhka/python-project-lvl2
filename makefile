insatll:
	poetry install

build:
	poetry build

lint:
	poetry run flake8 gendiff
	poetry run flake8 tests

tests:
	poetry run pytest

cov-tests:
	poetry run coverage report -m

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-force-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

.PHONY: tests