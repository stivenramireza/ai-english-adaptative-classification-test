from flask import Flask
from flask_restplus import Resource, Api, fields, marshal
from flask_restplus import reqparse
import model
import cat
import numpy as np


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
        # Choose a random ability level for the current Student.
        theta = np.random.uniform(low=-6, high=6)
        # According to te previous selected random ability choose the next item to be exposed.
        n_item = np.random.randint(_cat.get_dataset_size() - 1)
        idx = np.random.randint(2)
        # Assume a uniform random response for the given question.
        response = [True, False][idx]
        _, n_item, quest, responses, _ = _cat.ask(n_item, response, theta)
        cur_est_theta, administered_items, response_vector, parts = _cat.get_current_test_status()
        # Send the new random item to the Student.
        data = {
            'question': {
                'n_item': int(n_item),
                'title': quest,
                'responses': [responses[0], responses[1], responses[2]],
                'ability': cur_est_theta,
                'administered_items': administered_items,
                'response_vector': response_vector,
                'parts': parts
            }
        }
        return data

@api.route('/test/next_question')
class NextQuestion(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('n_item', type=int, required=True, help='Question id cannot be converted')
        parser.add_argument('n_response', type=int, required=True, help='Response id cannot be converted')
        parser.add_argument('ability', type=float, required=True, help='Ability cannot be converted')
        parser.add_argument('response_vector', type=list, help='Response vector cannot be converted', location='json', default=[])
        parser.add_argument('administered_items', type=list, help='Administered items cannot be converted', location='json', default=[])
        parser.add_argument('parts', type=list, help='Parts cannot be converted', location='json', default=[])
        args = parser.parse_args()
        n_item = args['n_item']
        response = args['n_response']
        ability = float(args['ability'])
        administered_items = args['administered_items']
        response_vector = args['response_vector']
        parts = args['parts']
        print(ability)
        _cat.set_current_test_status(administered_items, response_vector, parts, n_item, response)
        _, n_item, quest, responses, _ = _cat.ask(n_item=-1, n_reponse=None, cur_est_theta=ability)
        cur_est_theta, administered_items, response_vector, parts = _cat.get_current_test_status()
        data = {
            'question': {
                'n_item': int(n_item),
                'title': quest,
                'responses': [responses[0], responses[1], responses[2]],
                'ability': cur_est_theta,
                'administered_items': administered_items,
                'response_vector': response_vector,
                'parts': parts
            }
        }
        return data


@api.route('/test/statistics')
class Statistics(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('c_part1', type=float, required=True, help='c_part1 cannot be converted')
        parser.add_argument('c_part2', type=float, required=True, help='c_part2 cannot be converted')
        parser.add_argument('c_part3', type=float, required=True, help='c_part3 id cannot be converted')
        args = parser.parse_args()
        c_part1, c_part2, c_part3 = args['c_part1'], args['c_part2'], args['c_part3']
        final_grade = np.sum([c_part1*.2, c_part2*.3, c_part3*.5])
        return {
            "student": {
                "final_grade": final_grade
            }
        }
@api.route('/test/statistics/level')
class StatisticsLevel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('c_part1', type=float, required=True, help='c_part1 cannot be converted')
        parser.add_argument('c_part2', type=float, required=True, help='c_part2 cannot be converted')
        parser.add_argument('c_part3', type=float, required=True, help='c_part3 id cannot be converted')
        args = parser.parse_args()
        c_part1, c_part2, c_part3 = args['c_part1'], args['c_part2'], args['c_part3']
        level = _model.predict([[c_part1, c_part2, c_part3]])
        print(level[0])
        return {
            "student": {
                "level": int(level[0])
            }
        }

if __name__ == "__main__":
    _model.train()
    _model.save_model()
    _model.load_model()
    print(_model.predict([[2.5, 3.7, 4]]))
    app.run(debug=True, port=5001, host='0.0.0.0')