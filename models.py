import datetime

import jwt
from flask_sqlalchemy import SQLAlchemy

from settings import SECRET_KEY
from utils import format_datetime as f_dt
from utils import sha512

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    nickname = db.Column(db.Unicode(32))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(255), unique=True, nullable=True)
    email_verified = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, default=datetime.datetime.now)
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)
    active = db.Column(db.Boolean, default=True)
    save_method = db.Column(db.String(32), default='normal')
    diary_password_hash = db.Column(db.String(128), nullable=True)

    diarys = db.relationship('Diary', backref='User', lazy='dynamic')

    def to_json(self):
        return {
            'id':
            self.id,
            'username':
            self.username,
            'nickname':
            self.nickname,
            'email':
            self.email,
            'date_joined':
            f_dt(self.date_joined),
            'last_login':
            f_dt(self.last_login),
            'active':
            self.active,
            'save_method':
            self.save_method,
            'diary_password_hash':
            self.save_method == 'aes' and self.diary_password_hash or ''
        }

    def __init__(self,
                 username,
                 password,
                 email=None,
                 nickname=None,
                 save_method='normal',
                 diary_password_hash=None):
        self.username = username
        self.password_hash = sha512(password)
        self.email = email
        self.nickname = nickname
        self.save_method = save_method if save_method in ('normal',
                                                          'aes') else 'normal'
        self.diary_password_hash = diary_password_hash

    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if user is None:
            return None
        if user.password_hash != sha512(password):
            return None
        return user

    def get_token(self):
        payload = {
            'user_id': self.id,
            'exp': datetime.datetime.now() + datetime.timedelta(days=1)
        }
        jwt_data = jwt.encode(payload=payload,
                              key=SECRET_KEY,
                              algorithm='HS256')
        if type(jwt_data) is bytes:
            # In case a outdated version of PyJWT is installed
            jwt_data = jwt_data.decode('utf-8')
        return f'JWT {jwt_data}'

    @staticmethod
    def check_token(token):
        try:
            payload = jwt.decode(jwt=token,
                                 key=SECRET_KEY,
                                 algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            if user.active:
                return user
            return None
        except jwt.ExpiredSignatureError:
            return None

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __repr__(self):
        return f'<User {self.username}>'


class Diary(db.Model):
    __tablename__ = 'diarys'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(127))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',
                           backref='Diary',
                           lazy='joined',
                           viewonly=True)
    tags = db.Column(db.Unicode(255))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now)
    public = db.Column(db.Boolean, default=False)
    cover = db.Column(db.String(511), nullable=True)

    def __init__(self, title, content, user_id, tags, public, cover):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.tags = tags
        self.public = public
        self.cover = cover

    def to_json(self, max_length=None, public=False):
        data = {
            'id': self.id,
            'title': self.title,
            'content':
            self.content[:max_length] if max_length else self.content,
            'tags': self.tags,
            'cover': self.cover,
            'create_time': f_dt(self.create_time),
            'update_time': f_dt(self.update_time),
            'public': self.public,
        }
        if public == False:
            data.update({
                'user': {
                    'id': self.user.id,
                    'username': self.user.username
                },
            })
        return data

    def __repr__(self):
        return f'<Diary {self.title}>'
