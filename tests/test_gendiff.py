from gendiff.scripts.gendiff import generate_diff


def generate_diff_test():
    file = open('./tests/fixtures/fixture_gendiff_test.txt', 'r')
    result = file.read()

    assert generate_diff('file1.json', 'file2.json') == str(result)


generate_diff_test()
