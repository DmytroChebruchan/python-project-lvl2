install:
	poetry build
	poetry install

gendiff:
	install
	poetry run gendiff
