from gendiff.scripts.gendiff import generate_diff


def test_generate_diff_json():
    file = open('./tests/fixtures/results/fixture_gendiff_test.txt', 'r')
    result = file.read()
    assert generate_diff('tests/fixtures/JSON/file1.json', 'tests/fixtures/JSON/file2.json') == str(result)

test_generate_diff_json()


def test_generate_diff_json_2():
    file = open('./tests/fixtures/results/fixture_gendiff_test_2.txt', 'r')
    result = file.read()
    assert generate_diff('tests/fixtures/JSON/file1_2.json', 'tests/fixtures/JSON/file2_2.json') == str(result)

test_generate_diff_json_2()


def test_generate_diff_json_plain():
    file = open('./tests/fixtures/results/fixture_gendiff_test_3.txt', 'r')
    result = file.read()
    assert generate_diff('tests/fixtures/JSON/file1_2.json', 'tests/fixtures/JSON/file2_2.json', format = 'plain') == str(result)

test_generate_diff_json_plain()