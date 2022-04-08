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

update:
	make build
	make publish
	make package-install

test:
	@poetry run python -m gendiff.scripts.gendiff -f 'JSON' file1.json file2.json

push:
	git add .
	git commit -m 'autocommit'
	git push