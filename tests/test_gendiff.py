from gendiff.scripts.gendiff import generate_diff

assert generate_diff() == '''{ 
  - "follow": false
    "host": hexlet.io
  - "proxy": 123.234.53.22
  - "timeout": 50
  + "timeout": 20
  + "verbose": true
}'''
