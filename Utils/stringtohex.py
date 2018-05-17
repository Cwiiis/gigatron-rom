#!/usr/bin/env python

from __future__ import print_function
import argparse

parser = argparse.ArgumentParser(description=
        'Convert a string into a sequence of hex values.',
        epilog='Example usage: %(prog)s "Hello World"')

parser.add_argument('string', nargs="+", help='A raw 24-bit RGB image')
args = parser.parse_args()

print('[def', end='')
for letter in args.string[0]:
  print(' $%02x#' % (ord(letter)), end='')
print(' $00#]')
