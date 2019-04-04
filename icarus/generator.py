import os
import re

import mistune
import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import Extension

import utils

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

    Code generation flow:
      1. Load config.yaml and store variables as `config.*`
      2. Render posts
        2.1 Render jinja variables (frontmatter and config variables)
        2.2 Render markdown
        2.3 Render `post.html` with content exposed as `post.content` and
            frontmatter variables as `post.*`
      3. Load and render pages
    """
    def __init__(self):
        self.context = dict()
        self.frontmatters = utils.Dict()
        FME = utils.partial_class(FrontMatterExtension, data=self.frontmatters)
        self.env = Environment(
            loader=FileSystemLoader(['pages', 'templates', 'posts']),
            autoescape=False,
            extensions=[FME])

    def _load_config(self):
        with open('config.yaml', 'r') as f:
            self.context['config'] = yaml.load(f.read())

    def _resolve_permalink(self, permalink, filename):
        pass

    def _render_posts(self):
        markdown_renderer = mistune.Markdown()
        for post in os.listdir('posts'):
            #with open(os.path.join('posts', post), 'r') as f:
            #    file_content = f.read()
            #jinja_markdown = self.env.from_string(file_content)
            jinja_markdown = self.env.get_template(post)
            markdown = jinja_markdown.render(
                config=self.context['config'], **self.frontmatters[post])
            content = markdown_renderer(markdown)
            self.frontmatters[post]['content'] = content
            output = self.env.get_template('post.html').render(
                post=self.frontmatters[post], config=self.context['config'])
            #_url = self._resolve_permalink(self.frontmatters[post].get('permalink'))
            self._write_to_dist(post, output)

    @staticmethod
    def _write_to_dist(path, content):
        with open(os.path.join(OUTPUT_DIR, path), 'w') as f:
            f.write(content)

    def generate(self):
        if os.path.exists(OUTPUT_DIR):
            os.removedirs(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR)
        self._load_config()
        self._render_posts()
