import random
import string
from typing import Any, Dict, Optional
from datetime import datetime

import factory
import orjson
from sqlalchemy.orm import Session

from app import crud
from app.dtos import UserForRegister, BlogForNew
from app.model import User, Blog
from tests.factory import UserFactory, BlogFactory


def create_random_user(session: Session, *, is_superuser=False, password=None) -> User:
    user_data: Dict[Any, Any] = factory.build(dict, FACTORY_CLASS=UserFactory)
    user_data.update({"is_superuser": is_superuser})
    if password:
        user_data.update({"password": password})
    user_in = UserForRegister(**user_data)
    created_user = crud.create_user(db_session=session, user_in=user_in)
    return created_user


def create_random_blog(
    session: Session,
    *,
    is_published: bool = False,
    author_id: Optional[int] = None,
    title: str = None,
) -> Blog:
    blog_dict: Dict[str, Any] = factory.build(dict, FACTORY_CLASS=BlogFactory)
    blog_dict.update({"is_published": is_published})
    if title:
        blog_dict.update({"title": title})
    blog_in = BlogForNew(**blog_dict)
    if author_id is None:
        user = create_random_user(session)
        author_id = user.id
    return crud.create_blog(session, new_blog=blog_in, author_id=author_id)

