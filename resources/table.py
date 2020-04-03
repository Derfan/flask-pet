from flask_restful import Resource, reqparse
from models.table import TableModel


class Table(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('seats', type=int, required=True, help='This field can not be blank')
    parser.add_argument('restaurant_id', type=int, required=True, help='This field can not be blank')

    def get(self, _id):
        table = TableModel.find_by_id(_id)

        return table.json() if table else ({'message': f'Table with id {_id} not found'}, 404)

    def post(self):
        data = self.parser.parse_args()
        new_table = TableModel(data['seats'], data['restaurant_id'])

        new_table.save_to_db()

        return new_table.json(), 201

    def delete(self, _id):
        table = TableModel.find_by_id(_id)

        if not table:
            return {'message': f'No table with id {_id}'}, 404

        table.delete_from_db()

        return {'message': f'Table with {_id} deleted'}


class Tables(Resource):
    def get(self):
        return {'tables': [table.json() for table in TableModel.query.all()]}
