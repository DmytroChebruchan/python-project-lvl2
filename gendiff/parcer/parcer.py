

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
