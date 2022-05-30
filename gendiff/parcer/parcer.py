import argparse


def parcer():
    parser = argparse.ArgumentParser(description='Generate diff')

    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-v', '--version')
    parser.add_argument('-f', '--format',
                        help='set format of output')
    result = [parser.parse_args().first_file,
              parser.parse_args().second_file,
              parser.parse_args().format]
    return result


# finder of format
def format_parcer(first_file):
    found_format = ''

    i = 0
    while i < len(first_file):
        if first_file[i] == '.':
            break
        i = i + 1
    found_format = str(first_file[i + 1:]).upper()

    formats = {'JSON': 'JSON',
               'YAML': 'YML',
               'YML': 'YML'}

    return formats.get(found_format)


def main():
    parcer()


if __name__ == '__main__':
    main()
