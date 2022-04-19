from gendiff.scripts.gendiff import generate_diff


def test_generate_diff_yaml():
    file = open('./tests/fixtures/fixture_gendiff_test.txt', 'r')
    result = file.read()
    assert generate_diff('tests/fixtures/file1.yml', 'tests/fixtures/file2.yml') == str(result)

def test_generate_diff_yaml_with_format_stated():
    file = open('./tests/fixtures/fixture_gendiff_test.txt', 'r')
    result = file.read()
    assert generate_diff('tests/fixtures/file1.yml', 'tests/fixtures/file2.yml', 'yml') == str(result)

test_generate_diff_yaml_with_format_stated()
test_generate_diff_yaml()
