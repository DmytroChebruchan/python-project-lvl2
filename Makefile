poetry_to_path:
	export PATH='$PATH:/Users/alexey/Library/Python/3.10/bin'

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

push:
	make lint
	poetry run pytest --cov-report term-missing --cov=gendiff tests/
	git add .
	git commit -m '$(M)'
	git push

lint:
	python3 -m flake8 gendiff

run:
	python3 -m gendiff.scripts.gendiff -f 'JSON' file1.json file2.json

run2:
	python3 -m gendiff.scripts.gendiff -f 'YML' file1.yml file2.yml

check:
	make lint
	poetry run pytest --cov-report term-missing --cov=gendiff tests/

man_test_json:
	python3 -m tests.test_gendiff_json file1.json file2.json

man_test_yml:
	python3 -m tests.test_gendiff_yml file1.yml file2.yml