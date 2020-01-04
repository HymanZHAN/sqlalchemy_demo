import random
import string
from datetime import datetime, timedelta

import factory
import orjson

from app.orm import Blog, User


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_blog_body(time=datetime.now()):
    body_dict = {
        "time": time,
        "blocks": [
            {"type": "header", "data": {"text": "Editor.js", "level": 2}},
            {
                "type": "paragraph",
                "data": {
                    "text": "Hey. Meet the new Editor. On this page you can see it in action — try "
                    "to edit this text."
                },
            },
            {"type": "header", "data": {"text": "Key features", "level": 3}},
            {
                "type": "list",
                "data": {
                    "style": "unordered",
                    "items": [
                        "It is a block-styled editor",
                        "It returns clean data output in JSON",
                        "Designed to be extendable and pluggable with a simple API",
                    ],
                },
            },
            {
                "type": "header",
                "data": {"text": "What does it mean «block-styled editor»", "level": 3},
            },
            {
                "type": "paragraph",
                "data": {
                    "text": 'Workspace in classic editors is made of a single contenteditable element, used to create different HTML markups. Editor.js <mark class="cdx-marker">workspace consists of separate Blocks: paragraphs, headings, images, lists, quotes, etc</mark>. Each of them is an independent contenteditable element (or more complex structure) provided by Plugin and united by Editor\'s Core.'  # noqa
                },
            },
            {
                "type": "paragraph",
                "data": {
                    "text": 'There are dozens of <a href="https://github.com/editor-js">ready-to-use Blocks</a> and the <a href="https://editorjs.io/creating-a-block-tool">simple API</a> for creation any Block you need. For example, you can implement Blocks for Tweets, Instagram posts, surveys and polls, CTA-buttons and even games.'  # noqa
                },
            },
            {
                "type": "header",
                "data": {"text": "What does it mean clean data output", "level": 3},
            },
            {
                "type": "paragraph",
                "data": {
                    "text": "Classic WYSIWYG-editors produce raw HTML-markup with both content data and content appearance. On the contrary, Editor.js outputs JSON object with data of each Block. You can see an example below"  # noqa
                },
            },
            {
                "type": "paragraph",
                "data": {
                    "text": 'Given data can be used as you want: render with HTML for <code class="inline-code">Web clients</code>, render natively for <code class="inline-code">mobile apps</code>, create markup for <code class="inline-code">Facebook Instant Articles</code> or <code class="inline-code">Google AMP</code>, generate an <code class="inline-code">audio version</code> and so on.'  # noqa
                },
            },
            {
                "type": "paragraph",
                "data": {
                    "text": "Clean data is useful to sanitize, validate and process on the backend."
                },
            },
            {"type": "delimiter", "data": {}},
            {
                "type": "paragraph",
                "data": {
                    "text": "We have been working on this project more than three years. Several large media projects help us to test and debug the Editor, to make it's core more stable. At the same time we significantly improved the API. Now, it can be used to create any plugin for any task. Hope you enjoy. 😏"  # noqa
                },
            },
            {
                "type": "image",
                "data": {
                    "file": {
                        "url": "https://capella.pics/6d8f1a84-9544-4afa-b806-5167d45baf7c.jpg"
                    },
                    "caption": "",
                    "withBorder": True,
                    "stretched": False,
                    "withBackground": False,
                },
            },
        ],
        "version": "2.15.0",
    }

    body: bytes = orjson.dumps(body_dict)
    return body


class UserFactory(factory.Factory):
    class Meta:
        model = User

    created_at = factory.LazyAttribute(lambda o: o.updated_at - timedelta(hours=1))
    updated_at = factory.LazyFunction(datetime.now)

    email = factory.Faker("email")
    username = factory.Sequence(lambda n: f"user_{n}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    password = random_lower_string()

    is_active = True
    is_superuser = False

    background = factory.Faker("job")
    interests = factory.Faker(
        "word",
        ext_word_list=[
            "web",
            "programming",
            "UI",
            "UX",
            "research",
            "ergonomics",
            "automobile",
            "design",
            "human-centered",
            "education",
            "environment",
        ],
    )
    bio = factory.Faker("paragraph", nb_sentences=3, variable_nb_sentences=True)


class BlogFactory(factory.Factory):
    class Meta:
        model = Blog

    title = factory.Faker(
        "sentence", nb_words=10, variable_nb_words=True, ext_word_list=None
    )
    subtitle = factory.Faker(
        "sentence", nb_words=10, variable_nb_words=True, ext_word_list=None
    )
    is_published = True
    body = random_blog_body()
