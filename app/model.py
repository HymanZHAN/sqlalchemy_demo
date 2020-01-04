from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class AuditableEntity:
    """
    Entity that records and update information about author, editor and created/edited time.
    """

    author_id: int
    editor_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Bookmark:
    """Entity model that represents a bookmark that a user created for some content."""

    bookmarker_id: int

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_bookmarked: bool = True

    blog_id: Optional[int] = None

    def __repr__(self) -> str:
        return f"<Bookmark by user (ID: {self.bookmarker_id})>"


@dataclass
class Blog(AuditableEntity):
    title: str = field(default_factory=str)
    subtitle: str = field(default_factory=str)
    is_published: bool = field(default_factory=lambda: False)
    body: str = field(default_factory=str)

    _bookmarks: List[Bookmark] = field(default_factory=list)
    _bookmark_count: int = field(default_factory=int)

    def __repr__(self) -> str:
        return f"<Blog '{self.title}' by user of id {self.author_id}>"

    @property
    def bookmarks(self) -> List[Bookmark]:
        return [bookmark for bookmark in self._bookmarks if bookmark.is_bookmarked]

    def add_bookmark(self, bookmark: Bookmark) -> None:
        self._bookmarks.append(bookmark)
        self._bookmark_count += 1


@dataclass
class User:
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    username: str = field(default_factory=str)
    hashed_password: str = field(default_factory=str)

    is_active: bool = field(default_factory=lambda: True)
    is_admin: bool = field(default_factory=lambda: False)
    is_superuser: bool = field(default_factory=lambda: False)

    background: Optional[str] = None
    interests: Optional[str] = None
    bio: Optional[str] = None

    blogs: List[Blog] = field(default_factory=list)
    bookmarks: List[Bookmark] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.username = self.email.split("@")[0]

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.email == other.email

    def __hash__(self) -> int:
        return hash(self.email)
