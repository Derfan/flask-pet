from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.restaurant import RestaurantModel


class Restaurant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field can not be blank')
    parser.add_argument('address', type=dict, required=False, default={})

    def get(self, _id):
        restaurant = RestaurantModel.find_by_id(_id)

        return restaurant.json() if restaurant else ({'message': 'Restaurant not found'}, 404)

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        new_restaurant = RestaurantModel(data['name'], data['address'].get('country', None), data['address'].get('city', None))

        new_restaurant.save_to_db()

        return new_restaurant.json(), 201

    @jwt_required()
    def put(self, _id):
        data = self.parser.parse_args()
        restaurant = RestaurantModel.find_by_id(_id)

        if restaurant:
            restaurant.name = data['name']
        else:
            RestaurantModel(data['name'], data['address'].get('country', None), data['address'].get('city', None))

        restaurant.save_to_db()

        return restaurant.json(), (200 if restaurant else 201)

    @jwt_required()
    def delete(self, _id):
        restaurant = RestaurantModel.find_by_id(_id)

        if not restaurant:
            return {'message': f'No restaurant with id {_id}'}, 404

        restaurant.delete_from_db()

        return {'message': f'Item with {_id} deleted'}


class Restaurants(Resource):
    def get(self):
        restaurants = list(map(lambda x: x.json(), RestaurantModel.query.all()))

        return {'restaurants': restaurants, 'length': len(restaurants)}
