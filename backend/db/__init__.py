from .models import (
    Config,
    Comment,
    User,
    Post,
    Subscribe
)


def up():
    Config.BASE.metadata.create_all(Config.ENGINE)


def down():
    Config.BASE.metadata.drop_all(Config.ENGINE)


def migrate():
    down()
    up()


def get_session():
    with Config.SESSION.begin() as session:
        yield session