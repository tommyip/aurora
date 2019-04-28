"""Aurora - a minimalist, blog-aware static site generator

usage:
    aurora create <project_name>
    aurora new <post_title>
    aurora build

options:
    -h --help  Show this screen.
    --version  Show version.

"""
import sys

from docopt import docopt

from aurora import __version__, scaffold
from aurora.generator import Generator


def cli():
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    args = docopt(__doc__, version=__version__)

    if args['create']:
        scaffold.create(args['<project_name>'])
    elif args['new']:
        scaffold.new(args['<post_title>'])
    elif args['build']:
        Generator().run()
