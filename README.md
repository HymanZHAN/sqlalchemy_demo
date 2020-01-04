# sqlalchemy_demo

To run the project, you need to have `pipenv` installed.

```bash
pip install pipenv
```
or
```bash
pip3 install pipenv
```

With `pipenv` installed, activate the virtual environment and install the dependencies:

```bash
pipenv shell
pipenv install --dev
```

Run the test:

```bash
pytest
```

The test is lcoated at `tests/test_blog.py`. To make the test fail, remove the `bookmakr = ` assignment at the first `crud.toggle_bookmark` call.

```bash
> pytest
===================================================================================== test session starts =====================================================================================
platform linux -- Python 3.7.5, pytest-5.3.2, py-1.8.1, pluggy-0.13.1
rootdir: /home/xzhan/Development/Projects/sqlalchemy_demo
collected 1 item                                                                                                                                                                              

tests/test_blog.py F                                                                                                                                                                    [100%]

========================================================================================== FAILURES ===========================================================================================
___________________________________________________________________________________ test_unbookmark_a_blog ____________________________________________________________________________________

session = <sqlalchemy.orm.session.Session object at 0x7f2980826ed0>

    def test_unbookmark_a_blog(session):
        author = create_random_user(session)
        blog = create_random_blog(session, is_published=True, author_id=author.id)
        bookmarker = create_random_user(session)
    
        # remove "bookmark = " below to make the test fail
        crud.toggle_bookmark(session, blog_id=blog.id, bookmarker_id=bookmarker.id)
    
        assert len(blog.bookmarks) == 1
    
        crud.toggle_bookmark(session, blog_id=blog.id, bookmarker_id=bookmarker.id)
    
>       assert len(blog.bookmarks) == 0
E       AssertionError: assert 1 == 0
E        +  where 1 = len([<Bookmark by user (ID: 3)>])
E        +    where [<Bookmark by user (ID: 3)>] = <Blog 'Partner population that else gas today kid fill product close real.' by user of id 2>.bookmarks

tests/test_blog.py:20: AssertionError
====================================================================================== 1 failed in 0.28s ======================================================================================
```
