import hashlib

from settings import SECRET_KEY


def sha512(content):
    hash = hashlib.sha512(content.encode("utf-8"))
    hash.update(SECRET_KEY.encode("utf-8"))
    return hash.hexdigest()


if __name__ == '__main__':
    print(sha512('123456'))
