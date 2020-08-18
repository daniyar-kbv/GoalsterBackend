import os, shutil


def visualization_document_path(instance, filename):
    return f'visualizations/{instance.id}/{filename}'


def delete_folder(document):
    path = os.path.abspath(os.path.join(document.path, '..'))
    if os.path.isdir(path):
        shutil.rmtree(path)


def delete_file(document):
    path = os.path.abspath(document.path)
    os.remove(path)
