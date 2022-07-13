import os
import pathlib
from urllib import parse

PATH = pathlib.Path(__file__).parent

MODE = os.environ.get('MODE', 'development')

with open(PATH / 'secret.key') as f:
    SECRET_KEY = f.read()

SQLALCHEMY = {
    'SQLALCHEMY_COMMIT_ON_TEARDOWN': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}

if MODE == 'development':
    DEBUG = True
    SQLALCHEMY.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite3',
        # 'SQLALCHEMY_ECHO': True,
    })
elif MODE == 'production':
    DEBUG = False
    DB_HOST = os.environ.get('DB_HOST', 'localhost:5432')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = parse.quote_plus(os.environ.get('DB_PASSWORD'))
    DB_DB = os.environ.get('DB_DB')
    SQLALCHEMY.update({
        'SQLALCHEMY_DATABASE_URI':
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DB}',
    })