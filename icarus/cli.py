"""Icarus - an intentionally minimal static site generator.

usage:
    icarus create <project_name>
    icarus build

options:
    -h --help  Show this screen.
    --version  Show version.

"""
import sys

from docopt import docopt

from icarus import __version__, scaffold
from icarus.generator import Generator


def cli():
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    args = docopt(__doc__, version=__version__)

    if args['create']:
        scaffold.init(args['<project_name>'])
    elif args['build']:
        Generator().run()
