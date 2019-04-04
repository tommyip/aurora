import argparse
import sys

import generator
import scaffold

parser = argparse.ArgumentParser(description='Icarus')
subparsers = parser.add_subparsers(dest='command')

parser_init = subparsers.add_parser('init', help='Create a new blog')
parser_init.add_argument('project_name', type=str, help='Name of the project')

args = parser.parse_args()
if not len(sys.argv) > 1:
    # Build static site
    gen = generator.Generator()
    gen.generate()

if args.command == 'init':
    scaffold.init(args.project_name)
