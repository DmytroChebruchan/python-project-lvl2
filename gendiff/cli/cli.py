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
