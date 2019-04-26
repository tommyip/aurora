import os

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
                f.write(folder_or_file['content'])  # TODO: Interpolation


def init(project_name):
    """ Project scaffolding as per `structure.yaml`.
    """
    try:
        os.makedirs(project_name)
        skeleton = os.path.join(os.path.dirname(__file__), 'structure.yaml')
        with open(skeleton, 'r') as f:
            structure = yaml.load(f.read())
        scaffold(structure, project_name)

    except OSError as e:
        print(e)
