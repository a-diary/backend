import flask_restful
from flask import Flask, g, request
from flask_migrate import Migrate

import settings
import views
from errors import FORBIDDEN, REQUIRE_LOGIN
from models import User, db

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config.update(settings.SQLALCHEMY)
db.init_app(app)
migrate = Migrate(app, db)


@app.before_request
def before_request():
    # Add request.json, request.args and request.form to g.values
    values = request.values.to_dict()
    if request.headers.get('Content-Type') == 'application/json':
        values.update(request.json or {})
    g.values = values

    # Add g.user
    g.user = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(' ')[1]
        user = User.check_token(token)
        g.user = user


@app.errorhandler(403)
def error_403(e):
    if g.user is None:
        return REQUIRE_LOGIN
    return FORBIDDEN


api = flask_restful.Api(app)

api.add_resource(views.UserView, '/user/<int:id>')
api.add_resource(views.UserListView, '/user')
api.add_resource(views.DiaryView, '/diary/<int:id>')
api.add_resource(views.DiaryListView, '/diary')

app.register_blueprint(views.blueprint)

if __name__ == '__main__':
    app.run(debug=settings.DEBUG)
