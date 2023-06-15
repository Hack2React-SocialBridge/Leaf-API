from pathlib import Path
from os import path, makedirs, remove, environ
from glob import glob


from leaf.tasks import resize_image


MEDIA_BASE_URL = environ.get("MEDIA_BASE_URL")
MEDIA_FOLDER = environ.get("MEDIA_FOLDER")


def get_resource_absolute_path(relative_resource_path: Path, media_folder: str = MEDIA_FOLDER):
    return Path("/", media_folder, *relative_resource_path.parts)


def create_media_resource(absolute_resource_path: Path, resource: bytes):
    directory = absolute_resource_path.parent
    if not path.exists(directory):
        makedirs(directory)
    with open(absolute_resource_path, "wb") as handler:
        handler.write(resource)


def flush_old_media_resources(absolute_resource_path: Path):
    old_user_images = glob(f"{str(absolute_resource_path.parent)}/*{str(absolute_resource_path.stem)}.*")
    for file in old_user_images:
        remove(file)


def get_media_image_url(relative_resource_path: Path, size: int, media_base_url: str = MEDIA_BASE_URL):
    return f"{media_base_url}/{str(relative_resource_path.parent)}/{size}_{relative_resource_path.name}"
