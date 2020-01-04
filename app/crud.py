from typing import Optional

from sqlalchemy.orm import Session

from app.dtos import BlogForNew, UserForRegister
from app.orm import Blog, Bookmark, User


def create_user(db_session: Session, *, user_in: UserForRegister) -> User:
    user = User(
        email=user_in.email,
        username=user_in.email.split("@")[0],
        hashed_password="fakehash" + (user_in.password),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        is_superuser=user_in.is_superuser,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get_by_email(db_session: Session, *, email: str) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()


def create_blog(db_session: Session, *, new_blog: BlogForNew, author_id: int) -> Blog:
    blog = Blog(author_id=author_id, **new_blog.dict())
    db_session.add(blog)
    db_session.commit()
    return blog


def toggle_bookmark(db_session: Session, *, blog_id: int, bookmarker_id: int) -> Bookmark:
    blog: Blog = db_session.query(Blog).get(blog_id)
    bookmark: Optional[Bookmark] = db_session.query(Bookmark).filter(
        Bookmark.blog_id == blog_id, Bookmark.bookmarker_id == bookmarker_id
    ).one_or_none()

    if bookmark is None:
        bookmark = Bookmark(bookmarker_id=bookmarker_id)
        blog.add_bookmark(bookmark)
        db_session.add(bookmark)
        db_session.commit()
        return bookmark

    bookmark.is_bookmarked = not bookmark.is_bookmarked
    blog._bookmark_count = len(blog.bookmarks)
    db_session.add(bookmark)
    db_session.add(blog)
    db_session.commit()
    return bookmark
