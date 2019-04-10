import os
import re
import shutil

import mistune
import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import Extension

from icarus import utils
from icarus.defaults import OUTPUT_DIR, PERMALINK


class FormatError(Exception):
    """ Raised when the format of a template is malformed.
    """
    pass


class FrontMatterExtension(Extension):
    """ Frontmatter are not rendered by Jinja, instead we parse them ourselves
    and give Jinja the resulting dictionary as context.
    """
    def __init__(self, environment, data=None):
        self.data = data
        super(FrontMatterExtension, self).__init__(environment)

    def preprocess(self, source, name, filename=None):
        matches = re.search(r'^(?:---(.*)---)?\s*(.*)$', source, re.DOTALL)
        base = os.path.dirname(filename)
        if matches:
            self.data[base][name] = yaml.load(matches.group(1) or '') or {}
        else:
            self.data[base][name] = {}

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
        self.frontmatters = utils.Dict(
            {'pages': {}, 'templates': {}, 'posts': {}})
        FME = utils.partial_class(FrontMatterExtension, data=self.frontmatters)
        self.env = Environment(
            loader=FileSystemLoader(['pages', 'templates', 'posts']),
            autoescape=False,
            extensions=[FME])

    def _load_config(self):
        with open('config.yaml', 'r') as f:
            self.context['config'] = yaml.load(f.read())

    def _resolve_post_permalink(self, permalink, filename):
        """ Resolves a permalink against a filename and its frontmatter and
        return a concrete path.

        For example, given a post with filename `2019-04-08-hello-world.md`
        with a frontmatter entry of `category: tech`, a permalink of
        `permalink: /blog/:category/:year/:month/:title` resolves as the
        path `/blog/tech/2019/04/hello-world.html`.
        This expects the filename to always be in the format
        `yyyy-mm-dd-title(-title)*.md`.
        """
        path = []
        category = self.frontmatters['posts'][filename].get('category')
        year, month, day, *titles = filename.replace('.md', '').split('-')
        for segment in permalink[1:].split('/'):
            if segment.startswith(':'):
                placeholder = segment[1:]
                if placeholder == 'year':
                    path.append(year)
                elif placeholder == 'month':
                    path.append(month)
                elif placeholder == 'day':
                    path.append(day)
                elif placeholder == 'category':
                    if category:
                        path.append(category)
                    else:
                        raise FormatError('Frontmatter does not contain a \
                            category variable but the permalink calls for it.')
                elif placeholder == 'title':
                    path.append('-'.join(titles))
                else:
                    raise FormatError(
                        'Unknown placeholder `{}`.'.format(placeholder))
            else:
                path.append(segment)

        return os.path.join(*path) + '.html'

    def _render_posts(self):
        markdown_renderer = mistune.Markdown()
        post_template = self.env.get_template('post.html')
        post_fm = self.frontmatters['templates'].get('post.html', {})
        permalink = post_fm.get(
            'permalink', self.context['config'].get('permalink', PERMALINK))

        for post in os.listdir('posts'):
            # Rendering
            jinjadown = self.env.get_template(post)
            markdown = jinjadown.render(config=self.context['config'],
                                        **self.frontmatters['posts'][post])
            html = markdown_renderer(markdown)
            self.frontmatters['posts'][post]['content'] = html
            output = post_template.render(
                self.context, post=self.frontmatters['posts'][post])

            # Distribution
            url = self._resolve_post_permalink(permalink, post)
            self.frontmatters['posts'][post]['url'] = url
            self._write_to_dist(url, output)

    def _render_pages(self):
        for page in os.listdir('pages'):
            template = self.env.get_template(page)
            html = template.render(self.context)
            self._write_to_dist(page, html)

    @staticmethod
    def _write_to_dist(path, content):
        full_path = os.path.join(OUTPUT_DIR, path)
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        with open(full_path, 'w') as f:
            f.write(content)

    def run(self):
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR)

        self._load_config()
        self._render_posts()
        self.context.update(self.frontmatters())
        self._render_pages()
