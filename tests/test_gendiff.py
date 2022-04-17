from gendiff.scripts.gendiff import generate_diff


def test_generate_diff_json():
    file = open('./tests/fixtures/fixture_gendiff_test.txt', 'r')
    result = file.read()
    assert generate_diff('file1.json', 'file2.json') == str(result)

test_generate_diff_json()


# def test_generate_diff_yaml():
#     file = open('./tests/fixtures/fixture_gendiff_test.txt', 'r')
#     result = file.read()
#     assert generate_diff('file1.yaml', 'file2.yaml') == str(result)

# test_generate_diff_yaml()