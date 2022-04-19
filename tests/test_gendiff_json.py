from gendiff.scripts.gendiff import generate_diff


def test_generate_diff_json():
    file = open('./tests/fixtures/results/fixture_gendiff_test.txt', 'r')
    result = file.read()
    assert generate_diff('tests/fixtures/JSON/file1.json', 'tests/fixtures/JSON/file2.json') == str(result)
    assert generate_diff('tests/fixtures/JSON/file1.json', 'tests/fixtures/JSON/file2.json', 'JSON') == str(result)

test_generate_diff_json()