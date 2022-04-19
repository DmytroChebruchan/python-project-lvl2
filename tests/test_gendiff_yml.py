from gendiff.scripts.gendiff import generate_diff


def test_generate_diff_yaml():
    file = open('./tests/fixtures/results/fixture_gendiff_test.txt', 'r')
    result = file.read()
    assert generate_diff('tests/fixtures/YML/file1.yml', 'tests/fixtures/YML/file2.yml') == str(result)
    assert generate_diff('tests/fixtures/YML/file1.yml', 'tests/fixtures/YML/file2.yml', 'yml') == str(result)

test_generate_diff_yaml()
