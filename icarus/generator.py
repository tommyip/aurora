import os
import re

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.ext import Extension

from . import utils

OUTPUT_DIR = 'dist'


class FrontMatterExtension(Extension):
    """ Frontmatter are not rendered by Jinja, instead we parse them ourselves
    and give Jinja the resulting dictionary as context.
    """
    def __init__(self, environment, data=None):
        self.data = data
        super(FrontMatterExtension, self).__init__(environment)

    def preprocess(self, source, name, _filename=None):
        matches = re.search(r'^(?:---(.*)---)?\s*(.*)$', source, re.DOTALL)
        if matches:
            self.data[name] = yaml.load(matches.group(1) or '')
        return matches.group(2)


class Generator:
    """ Generate the static site!
    """
    def __init__(self):
        self.frontmatters = utils.Dict()
        FME = utils.partial_class(FrontMatterExtension, data=self.frontmatters)
        self.env = Environment(
            loader=FileSystemLoader(['pages', 'templates']),
            autoescape=select_autoescape(['html']),
            extensions=[FME])

        with open('config.yaml', 'r') as f:
            self.config = yaml.load(f.read())

    def generate(self):
        os.makedirs(OUTPUT_DIR)
        for page in os.listdir('pages'):
            template = self.env.get_template(page)
            with open(os.path.join(OUTPUT_DIR, page), 'w') as f:
                f.write(template.render())
