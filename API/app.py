from flask import Flask
from flask_restplus import Resource, Api, fields, marshal
from flask_restplus import reqparse
import model
import cat
import numpy as np
import json


app = Flask(__name__)
api = Api(app)

_model = model.Model()
_cat = cat.CAT()


quest_res_model = {
    'n_item': fields.Integer,
    'title': fields.String,
    'responses': fields.List(fields.Integer)
}

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/test/prestart')
class PreStart(Resource):
    def get(self):
        _cat = cat.CAT()
        theta = np.random.normal(loc=4.7, scale=1.3)
        n_item = np.random.randint(_cat.get_dataset_size() - 1)
        idx = np.random.randint(2)
        response = [True, False][idx]
        n_item, quest, responses, _ = _cat.ask(n_item, response)
        print((n_item, quest))
        data = {
            'question': {
                'n_item': int(n_item),
                'title': quest,
                'responses': [responses[0], responses[1], responses[2]]

            }
        }
        return data

@api.route('/test/next_question')
class NextQuestion(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('n_item', type=int, required=True, help='Question id cannot be converted')
        parser.add_argument('n_response', type=int, required=True, help='Response id cannot be converted')
        args = parser.parse_args()
        n_item, n_response = args['n_item'], args['n_response']
        n_item, quest, responses, _ = _cat.ask(n_item, n_response)
        data = {
            'question': {
                'n_item': int(n_item),
                'title': quest,
                'responses': [responses[0], responses[1], responses[2]]

            }
        }
        return data
@api.route('/test/statistics')
class Statistics(Resource):
    def get(self):
        _, __, ___ = _cat.get_statistics()
        return {
            'part1': _,
            'part2': __,
            'part3': ___
        }
@api.route('/test/statistics/level')
class StatisticsLevel(Resource):
    def get(self):
        _, __, ___ = _cat.get_statistics()
        return {
            'level': _model.predict([[_, __, ___]])
        }

if __name__ == "__main__":
    _model.load_model()
    app.run(debug=True, port=5001, host='0.0.0.0')