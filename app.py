from flask import Flask, request, jsonify
from flask_restful import Api

import settings
from models import db, User
import views

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)
api = Api(app)

api.add_resource(views.UserView, '/user/<string:name>')
api.add_resource(views.UserListView, '/user')

app.register_blueprint(views.blueprint)

if __name__ == '__main__':
    app.run(debug=True)
