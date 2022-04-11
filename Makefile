build:
	export PATH=$PATH:$HOME/.poetry/bin
	poetry build

publish:
	poetry publish --dry-run -u ' ' -p ' '

install:
	python3 -m pip install --user dist/*.whl
	export PATH=$PATH:$HOME/Library/Python/3.10/bin

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl
	export PATH=$PATH:$HOME/Library/Python/3.10/bin

update:
	make build
	make publish
	make package-install

run:
	@poetry run python -m gendiff.scripts.gendiff -f 'JSON' file1.json file2.json

test:
	@poetry run python -m tests.test_gendiff

push:
	git add .
	git commit -m 'autocommit'
	git push

lint:
	@python3 -m flake8 gendiff