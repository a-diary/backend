import pathlib

PATH = pathlib.Path(__file__).parent

with open(PATH / 'secret.key') as f:
    SECRET_KEY = f.read()
