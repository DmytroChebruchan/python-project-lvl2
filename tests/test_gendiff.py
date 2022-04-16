from gendiff.scripts.gendiff import generate_diff


def test_generate_diff():
    file = open('./tests/fixtures/fixture_gendiff_test.txt', 'r')
    result = file.read()
    assert generate_diff('file1.json', 'file2.json') == str(result)

test_generate_diff()