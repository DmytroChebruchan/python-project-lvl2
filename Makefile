test:
	gendiff tests/fixtures/JSON/file1_2.json tests/fixtures/JSON/file2_2.json

build:
	poetry build

publish:
	poetry publish --dry-run -u ' ' -p ' '

install:
	python3 -m pip install --user dist/*.whl
	export PATH=$$PATH:$$HOME/Library/Python/3.10/bin

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl
	export PATH=$$PATH:/Users/alexey/Library/Python/3.10/bin

update:
	make build
	make publish
	make package-install

removed:
	make lint
	poetry run pytest --cov-report term-missing --cov=gendiff tests/

push:
	git add .
	git commit -m '$(M)'
	git push

lint:
	python3 -m flake8 gendiff

run:
	@python3 -m gendiff.scripts.gendiff -f 'JSON' tests/fixtures/JSON/file1_3.json tests/fixtures/JSON/file2_3.json

run2:
	python3 -m gendiff.scripts.gendiff -f 'YML' tests/fixtures/JSON/file1.yml tests/fixtures/JSON/file2.yml

check:
	make lint
	poetry run pytest --cov-report term-missing --cov=gendiff tests/

man_test_json:
	python3 -m tests.test_gendiff_json tests/fixtures/JSON/file1.json tests/fixtures/JSON/file2.json

man_test_yml:
	python3 -m tests.test_gendiff_yml tests/fixtures/JSON/file1.yml tests/fixtures/JSON/file2.yml
