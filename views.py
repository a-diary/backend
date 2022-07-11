from flask import Blueprint
from flask_restful import Resource, reqparse
from models import db, User
from utils import sha512

LOCATIONS = ('args', 'form', 'json')

blueprint = Blueprint('main', __name__)


class UserView(Resource):
    def get(self, name):
        return {
            'user': name,
            'id': User.query.filter_by(username=name).first().id,
        }

    # def post(self, name):
    #     return {'user': name}

    # def put(self, name):
    #     return {'user': name}

    # def delete(self, name):
    #     return {'user': name}


class UserListView(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                            type=str,
                            required=True,
                            location=LOCATIONS)
        parser.add_argument('password',
                            type=str,
                            required=True,
                            location=LOCATIONS)
        self.parser = parser
        self.args = parser.parse_args()

    def get(self):
        return self.args

    def post(self):
        username = self.args['username']
        password = self.args['password']
        if User.query.filter_by(username=username).first() is not None:
            return {'status': 'error', 'message': '用户名已存在'}
        user = User(username=username, password_hash=sha512(password))
        db.session.add(user)
        db.session.commit()
        return self.args


@blueprint.route('/index')
def index():
    return 'index'
