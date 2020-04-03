from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('login', type=str, required=True, help='This field can not be blank')
    parser.add_argument('password', type=str, required=True, help='This field can not be blank')

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_key('login', data['login']):
            return {'message': f'User with login {data["login"]} already exist'}, 400

        new_user = UserModel(**data)

        new_user.save_to_db()

        return {'message': f'{new_user.login} has been created!'}, 201
