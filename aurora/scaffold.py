import os
import sys
from datetime import datetime

import yaml


def scaffold(objects, base):
    for folder_or_file in objects:
        if 'path' in folder_or_file:
            directory = os.path.join(base, folder_or_file['path'])
            os.makedirs(directory, exist_ok=True)
            scaffold(folder_or_file['subdirectory'], directory)
        elif 'filename' in folder_or_file:
            filename = os.path.join(base, folder_or_file['filename'])
            with open(filename, 'w') as f:
                f.write(folder_or_file['content'])


def create(project_name):
    """ Project scaffolding as per `structure.yaml`.
    """
    try:
        os.makedirs(project_name)
        skeleton = os.path.join(os.path.dirname(__file__), 'structure.yaml')
        with open(skeleton, 'r') as f:
            structure = yaml.load(f.read())
        scaffold(structure, project_name)

    except OSError:
        sys.exit('Directory with name `' + project_name + '` already exist.')


def new(post_title):
    """ Generate a new post with title `post_title` and current date.
    """
    date = datetime.today().strftime('%Y-%m-%d')
    post_name = '{}-{}.md'.format(date, post_title)
    output_path = os.path.join('posts', post_name)

    if os.path.exists(output_path):
        sys.exit('You have already created a post with this title today.')

    humanize_post_title = post_title.replace('-', ' ').capitalize()
    with open(output_path, 'w') as f:
        f.write('---\ntitle: {}\n---\n'.format(humanize_post_title))
