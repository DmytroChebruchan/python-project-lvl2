from gendiff.scripts.gendiff import generate_diff


def test_generate_diff_json():
    file = open('./tests/fixtures/fixture_gendiff_test.txt', 'r')
    result = file.read()
    assert generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.json') == str(result)

def test_generate_diff_json_with_format():
    file = open('tests/fixtures/fixture_gendiff_test.txt', 'r')
    result = file.read()
    assert generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.json', 'JSON') == str(result)

test_generate_diff_json()
test_generate_diff_json_with_format()