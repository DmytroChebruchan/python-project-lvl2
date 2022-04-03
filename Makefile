build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl
	export PATH=$PATH:$HOME/Library/Python/3.10/bin
