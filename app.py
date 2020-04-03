from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from db import db
from security import authenticate, identity as identity_func
from resources.table import Table, Tables
from resources.restaurant import Restaurants, Restaurant
from resources.user import UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config["JWT_AUTH_USERNAME_KEY"] = 'login'
app.secret_key = 'SECRET_KEY'

api = Api(app)
jwt = JWT(app, authenticate, identity_func)


@app.before_first_request
def create_table():
    db.create_all()


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
       'message': error.description,
       'code': error.status_code
    }), error.status_code


api.add_resource(UserRegister, '/register')
api.add_resource(Restaurants, '/restaurants')
api.add_resource(Restaurant, '/restaurant', '/restaurant/<string:_id>')
api.add_resource(Table, '/table', '/table/<string:_id>')
api.add_resource(Tables, '/tables')

if __name__ == "__main__":
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
