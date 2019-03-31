import os
import yaml

def scaffold(objects, base):
    for folder_or_file in objects:
        if 'path' in folder_or_file:
            directory = os.path.join(base, folder_or_file['path'])
            os.makedirs(directory, exist_ok=True)
            scaffold(folder_or_file['subdirectory'], directory)
        elif 'filename' in folder_or_file:
            with open(os.path.join(base, folder_or_file['filename']), 'w') as f:
                f.write(folder_or_file['content'])  # TODO: Interpolation

def new(project_name):
    """ Project scaffolding as per `structure.yaml`.
    """
    try:
        os.makedirs(project_name)
        with open('structure.yaml', 'r') as f:
            structure = yaml.load(f.read())
        scaffold(structure, project_name)

    except OSError as e:
        print(e)

if __name__ == '__main__':
    new("sample")
