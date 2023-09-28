from __future__ import annotations

from glob import glob
from os import makedirs, path, remove
from pathlib import Path
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from starlette import status

from leaf.config.config import Settings, get_settings


def get_resource_absolute_path(
    relative_resource_path: Path,
    settings: Settings = Depends(get_settings),
):
    return Path("/", settings.MEDIA_FOLDER, *relative_resource_path.parts)


def create_media_resource(absolute_resource_path: Path, file: bytes):
    directory = absolute_resource_path.parent
    if not path.exists(directory):
        makedirs(directory)
    with open(absolute_resource_path, "wb") as handler:
        handler.write(file)


def flush_old_media_resources(absolute_resource_path: Path):
    old_user_images = glob(
        f"{str(absolute_resource_path.parent)}/*{str(absolute_resource_path.stem)}.*",
    )
    for file in old_user_images:
        remove(file)


def get_media_image_url(
    relative_resource_path: Path,
    size: int | None = None,
):
    settings = get_settings()
    return f"{settings.MEDIA_BASE_URL}/{str(relative_resource_path.parent)}/{size if size else list(settings.IMAGE_SIZES.values())[0][1]}_{relative_resource_path.name}"


async def get_image_size(
    image_size: str = Header(default=None),
) -> int:
    settings = get_settings()
    if image_size is None:
        return list(settings.IMAGE_SIZES.values())[0][1]
    elif image_size in settings.AVAILABLE_IMAGE_SIZES:
        return settings.IMAGE_SIZES[image_size][1]

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Wrong image size! Available sizes are: {settings.AVAILABLE_IMAGE_SIZES}",
    )
