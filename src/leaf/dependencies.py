from os import environ
from typing import Annotated

from fastapi import Header, HTTPException, status

AVAILABLE_IMAGE_SIZES = environ.get("AVAILABLE_IMAGE_SIZES").split(",")
IMAGE_SIZES = {size: environ.get(f"{size.upper()}_IMAGE_SIZE").split("x") for size in AVAILABLE_IMAGE_SIZES}


async def get_image_size(image_size: Annotated[str, Header(...)]):
    if image_size in AVAILABLE_IMAGE_SIZES:
        return IMAGE_SIZES[image_size][1]

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Wrong image size! Available sizes are: {AVAILABLE_IMAGE_SIZES}")
