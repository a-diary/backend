import datetime
import hashlib
import random

import settings

CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
SYMBOLS = '!@#$%^&*()_+-=[]{}|;:,./<>?\'\"'


def random_string(length=32, symbols=False):
    choices = CHARACTERS
    if symbols:
        choices += SYMBOLS
    return ''.join(random.choice(choices) for i in range(length))


def sha512(content):
    hash = hashlib.sha512(content.encode("utf-8"))
    hash.update(settings.SECRET_KEY.encode("utf-8"))
    return hash.hexdigest()


def format_datetime(dt: datetime.datetime):
    dt = dt.astimezone()
    return dt.isoformat()


if __name__ == '__main__':
    print(sha512('123456'))
