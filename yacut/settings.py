import os
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        default="sqlite:///db.sqlite3"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


# Константы

MAX_ORIGINAL_LINK_LENGTH = 128
MAX_CUSTOM_ID_LENGTH = 16
MIN_LENGTH = 1
ALL_CHARS = string.ascii_letters + string.digits
