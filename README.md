[![Actions Status](https://github.com/DmitriyChebruchan/python-project-lvl2/workflows/hexlet-check/badge.svg)](https://github.com/DmitriyChebruchan/python-project-lvl2/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/54b91ece1062d51d180e/maintainability)](https://codeclimate.com/github/DmitriyChebruchan/python-project-lvl2/maintainability)
[![linter_check](https://github.com/DmitriyChebruchan/python-project-lvl2/workflows/linter-check/badge.svg)](https://github.com/DmitriyChebruchan/python-project-lvl2/actions/workflows/linter_check.yml)
[![pytest_check](https://github.com/DmitriyChebruchan/python-project-lvl2/workflows/pytest/badge.svg)](https://github.com/DmitriyChebruchan/python-project-lvl2/actions/workflows/pytest.yml)

## Description
Gendiff is a module for generating defference between 2 JSON or YML files.
Format is detected automaticaly. There are two options of result output:
plain and stylish. When output is plain, difference is shown in line, when
output is stylish, difference is shown in same format as input files.

## Instruction of installation for users
    pip install https://github.com/user/repo.git@branch

## Instruction of installation for developers
    git clone https://github.com/DmitriyChebruchan/python-project-lvl2

    cd python-project-lvl2

    make update

    gendiff -h
***
## Asciinemas of usage
Difference between 2 simple JSON files returned in 'stylish' format
    gendiff tests/fixtures/JSON/file1.json tests/fixtures/JSON/file2.json
[![asciicast](https://asciinema.org/a/499555.svg)](https://asciinema.org/a/499555)

Difference between 2 YML files returned in 'stylish' format
    gendiff tests/fixtures/YML/file1.yml tests/fixtures/YML/file2.yml
[![asciicast](https://asciinema.org/a/499635.svg)](https://asciinema.org/a/499635)

Difference between 2 complex JSON files returned in 'stylish' format
    gendiff tests/fixtures/JSON/file1_2.json tests/fixtures/JSON/file2_2.json
[![asciicast](https://asciinema.org/a/499636.svg)](https://asciinema.org/a/499636)

Difference between 2 complex JSON files returned in 'plain' format
    gendiff --format plain tests/fixtures/JSON/file1_2.json tests/fixtures/JSON/file2_2.json
[![asciicast](https://asciinema.org/a/499637.svg)](https://asciinema.org/a/499637)