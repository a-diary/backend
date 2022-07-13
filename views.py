import datetime
from os import abort

from flask import Blueprint, abort, g
from flask_restful import Resource

from errors import REQUIRE_LOGIN
from models import Diary, User, db
from utils import sha512

LOCATIONS = ('args', 'form', 'json')

blueprint = Blueprint('main', __name__)


class UserView(Resource):
    def put(self, id):
        user = User.query.get(id)
        user.nickname = g.values['nickname']
        user.email = g.values['email']
        if g.values.get('password_old') and g.values.get('password_new'):
            if user.password_hash != sha512(g.values['password_old']):
                return {'status': 'error', 'message': '原密码错误'}
            user.password_hash = sha512(g.values['password_new'])
        db.session.add(user)
        db.session.commit()
        return {'status': 'success', 'user': user.to_json()}


class UserListView(Resource):
    def post(self):
        user = User(username=g.values['username'],
                    password=g.values['password'],
                    email=g.values['email'],
                    nickname=g.values['nickname'],
                    save_method=g.values['save_method'],
                    diary_password_hash=g.values['diary_password_hash'])
        db.session.add(user)
        db.session.commit()
        return {'status': 'success', 'user': user.to_json()}


@blueprint.route('/user/login', methods=['POST'])
def user_login():
    user = User.login(g.values['username'], g.values['password'])
    if user is None:
        return {'status': 'error', 'message': '用户名或密码错误'}
    elif not user.active:
        return {'status': 'error', 'message': '用户已被封禁'}
    user.last_login = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
    return {
        'status': 'success',
        'user': user.to_json(),
        'jwt': user.get_token()
    }


class DiaryView(Resource):
    def get(self, id):
        diary = Diary.query.get(id)
        if (not g.user or diary.user_id != g.user.id) and not diary.public:
            abort(404)
        return {
            'status':
            'success',
            'data':
            diary.to_json(public=(not g.user or diary.user_id != g.user.id))
        }

    def put(self, id):
        if not g.user:
            return REQUIRE_LOGIN
        diary = g.user.diarys.filter_by(id=id).first()
        if diary is None:
            abort(404)
        diary.title = g.values['title']
        diary.content = g.values['content']
        diary.tags = g.values['tags']
        diary.public = g.values['public']
        diary.cover = g.values['cover']
        db.session.add(diary)
        db.session.commit()
        return {'status': 'success', 'data': diary.to_json()}


class DiaryListView(Resource):
    def get(self):
        public = g.values.get('source') == 'diaryPublicList'
        if not public and not g.user:
            return REQUIRE_LOGIN
        page = int(g.values.get('page', 1))
        per_page = g.values.get('per_page', 20)
        if public:
            query = Diary.query.filter_by(public=True)
        else:
            query = g.user.diarys
        pagination = query.order_by(Diary.id.desc()).paginate(page,
                                                              per_page,
                                                              error_out=False)
        items = pagination.items
        for i in range(len(items)):
            items[i] = items[i].to_json(max_length=100, public=public)
        return {'status': 'success', 'data': items, 'total': pagination.total}

    def post(self):
        if not g.user:
            return REQUIRE_LOGIN
        diary = Diary(user_id=g.user.id,
                      title=g.values['title'],
                      content=g.values['content'],
                      tags=g.values['tags'],
                      public=g.values['public'],
                      cover=g.values['cover'])
        db.session.add(diary)
        db.session.commit()
        return {'status': 'success', 'diary': diary.to_json()}


@blueprint.route('/index')
def index():
    print(type(User.query.all()))
    return 'index'
