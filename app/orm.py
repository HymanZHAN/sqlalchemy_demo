from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapper, relationship

from app.db import Base
from app.model import Blog, Bookmark, User

bookmark_table = Table(
    "bookmark",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("bookmarker_id", Integer, ForeignKey("user.id")),
    Column("created_at", TIMESTAMP(timezone=True), default=datetime.now),
    Column("updated_at", TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now,),
    Column("is_bookmarked", Boolean, default=True),
    Column("blog_id", ForeignKey("blog.id"), nullable=True),
)

mapper(
    Bookmark,
    bookmark_table,
    properties={
        "bookmarker": relationship(User, back_populates="bookmarks"),
        "blog": relationship(Blog, back_populates="_bookmarks"),
    },
)


blog_table = Table(
    "blog",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("author_id", Integer, ForeignKey("user.id")),
    Column("editor_id", Integer, ForeignKey("user.id")),
    Column("created_at", TIMESTAMP(timezone=True), default=datetime.now),
    Column("updated_at", TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now,),
    Column("title", String, unique=True, index=True, nullable=False),
    Column("subtitle", String),
    Column("is_published", Boolean, default=False),
    Column("body", String),
    Column("_bookmark_count", Integer, default=0),
)


mapper(
    Blog,
    blog_table,
    properties={
        "author": relationship(User, back_populates="blogs", foreign_keys=[blog_table.c.author_id]),
        "last_edited_by": relationship(User, foreign_keys=[blog_table.c.editor_id]),
        "_bookmarks": relationship(Bookmark, back_populates="blog"),
    },
)

user_table = Table(
    "user",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("created_at", TIMESTAMP(timezone=True), default=datetime.now),
    Column("updated_at", TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now,),
    Column("email", String, unique=True, index=True, default=""),
    Column("username", String, unique=True, index=True),
    Column("first_name", String, index=True),
    Column("last_name", String, index=True),
    Column("hashed_password", String, default=""),
    Column("is_active", Boolean(), default=True),
    Column("is_admin", Boolean(), default=False),
    Column("is_superuser", Boolean(), default=False),
    Column("background", String(30)),
    Column("interests", String(30)),
    Column("bio", String),
)

mapper(
    User,
    user_table,
    properties={
        "blogs": relationship(Blog, back_populates="author", foreign_keys=[blog_table.c.author_id]),
        "bookmarks": relationship(
            Bookmark, back_populates="bookmarker", foreign_keys=[bookmark_table.c.bookmarker_id],
        ),
    },
)
