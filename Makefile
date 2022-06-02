pytest:
	poetry run pytest --cov-report term-missing --cov=gendiff tests/

man_test_json:
	python3 -m tests.test_gendiff_json tests/fixtures/JSON/file1.json tests/fixtures/JSON/file2.json

man_test_yml:
	python3 -m tests.test_gendiff_yml tests/fixtures/JSON/file1.yml tests/fixtures/JSON/file2.yml

build:
	poetry build

publish:
	poetry publish --dry-run -u ' ' -p ' '

install:
	python3 -m pip install --user dist/*.whl

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl

lint:
	@poetry run flake8

update:
	make build
	make publish
	make package-install

push:
	make lint
	poetry run pytest --cov-report term-missing --cov=gendiff tests/
	git add .
	git commit -m '$(M)'
	git push

check:
	make lint
	pytest