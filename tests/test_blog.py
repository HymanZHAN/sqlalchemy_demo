# type: ignore[attr-defined]

from tests.utils import create_random_user, create_random_blog

from app import crud


def test_unbookmark_a_blog(session):
    author = create_random_user(session)
    blog = create_random_blog(session, is_published=True, author_id=author.id)
    bookmarker = create_random_user(session)
    bookmark = crud.toggle_bookmark(session, blog_id=blog.id, bookmarker_id=bookmarker.id)

    assert len(blog.bookmarks) == 1

    crud.toggle_bookmark(session, blog_id=blog.id, bookmarker_id=bookmarker.id)

    assert len(blog.bookmarks) == 0
