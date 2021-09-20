import os, shutil


def visualization_document_path(instance, filename):
    return f'visualizations/{instance.id}/{filename}'


def avatar_document_path(instance, filename):
    return f'avatars/{filename}'


def celebrity_avatar_document_path(instance, filename):
    return f'celebrity_avatars/{filename}'


def knowledge_image_path(instance, filename):
    return f'knowledge_images/{filename}'


def knowledge_story_image_path(instance, filename):
    return f'knowledge_story_images/{filename}'


def delete_folder(document):
    path = os.path.abspath(os.path.join(document.path, '..'))
    if os.path.isdir(path):
        shutil.rmtree(path)


def delete_file(document):
    path = os.path.abspath(document.path)
    os.remove(path)
