from __future__ import annotations

from typing import Optional

from sqlalchemy import update
from sqlalchemy.orm import Session, joinedload

from leaf.media import get_media_image_url
from leaf.models import User
from leaf.schemas.users import GroupProfileSchema, UserSchema


def get_user_by_email(
    db: Session,
    email: str,
    image_size: Optional[int] = None,
) -> Optional[UserSchema]:
    user = (
        db.query(User)
        .options(joinedload(User.groups))
        .filter(User.email == email)
        .first()
    )

    if user:
        groups = (
            [GroupProfileSchema(id=group.id, name=group.name) for group in user.groups]
            if user.groups
            else []
        )
        permissions = user.mapped_permissions
        user_image = None
        if profile_image := user.profile_image:
            user_image = (get_media_image_url(profile_image, image_size),)

        user_data = user.__dict__
        del user_data["permissions"]
        del user_data["groups"]
        del user_data["hashed_password"]
        user_data.pop("profile_image", None)

        return UserSchema(
            **user_data,
            profile_image=user_image,
            permissions=permissions,
            groups=groups,
        )
    return None


def get_active_user_by_email(
    db: Session,
    email: str,
    image_size: Optional[int] = None,
) -> UserSchema:
    user = (
        db.query(User)
        .options(joinedload(User.groups))
        .filter(
            User.disabled == False,
            User.email == email,
        )
        .first()
    )
    if user:
        groups = (
            [GroupProfileSchema(id=group.id, name=group.name) for group in user.groups]
            if user.groups
            else []
        )
        permissions = user.mapped_permissions
        user_image = None
        if profile_image := user.profile_image:
            user_image = (get_media_image_url(profile_image, image_size),)

        user_data = user.__dict__
        del user_data["permissions"]
        del user_data["groups"]
        del user_data["hashed_password"]
        user_data.pop("profile_image", None)

        return UserSchema(
            **user_data,
            profile_image=user_image,
            permissions=permissions,
            groups=groups,
        )


def create_one(db: Session, **user_props) -> User:
    db_user = User(**user_props)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_one(db: Session, user_email: str, **user_props) -> None:
    db.execute(
        update(User)
        .where(
            User.email == user_email,
        )
        .values(**user_props),
    )
    db.commit()
