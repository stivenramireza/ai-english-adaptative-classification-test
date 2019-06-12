from flask import Flask
from flask_restplus import Resource, Api, fields, marshal
from flask_restplus import reqparse
import model
import cat_pre
import numpy as np


app = Flask(__name__)
api = Api(app)

_model = model.Model()
_cat = cat_pre.CatPre()


quest_res_model = {
    'n_item': fields.Integer,
    'title': fields.String,
    'responses': fields.List(fields.Integer)
}

@api.route('/hello')
class HelloWorld(Resource):
    """
        Testing API.
    """
    def get(self):
        return {'hello': 'world'}

@api.route('/test/prestart')
class PreStart(Resource):
    """
        Pre start the test
    """
    def get(self):
        """
        Obtains the first question for a student.
        :return:
        """
        _cat = cat_pre.CatPre()
        # Choose a random ability level for the current Student.
        #theta = np.random.uniform(low=-1, high=0.3)
        # According to te previous selected random ability choose the next item to be exposed.
        #part1 = _cat.get_part_1()
        #idxs = part1.index
        #n_item_p = idxs[np.random.randint(len(idxs))] // 3
        #print(n_item_p)
        #idx = np.random.randint(2)
        # Assume a uniform random response for the given question.
        #response = [True, False][idx]
        #_, n_item, quest, responses, _ = _cat.ask(n_item_p, response, theta)
        #print("Ok")
        #cur_est_theta, administered_items, response_vector, parts = _cat.get_current_test_status()
        #print("Ok1")
        # Send the new random item to the Student.
        ai, rv, ps, q, r, ni = _cat.next_item()
        data = {
            'question': {
                'n_item': int(ni),
                'title': q,
                'responses': [r[0], r[1], r[2]],
                'ability': 0.0,
                'administered_items': ai,
                'response_vector': rv,
                'parts': ps
            }
        }
        return data

@api.route('/test/next_question')
class NextQuestion(Resource):
    """
        Gives the next question, according to the actual behavior of a student.
    """
    def post(self):
        """
        Obtains the current student behaviour and returns the next best question for her/him.
        :return:
        """
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
        _cat.set_current_test_status(administered_items, response_vector, parts)
        ai, rv, ps, q, r, ni = _cat.next_item(n_item, response)
        data = {
            'question': {
                'n_item': int(ni),
                'title': q,
                'responses': [r[0], r[1], r[2]],
                'ability': 0.0,
                'administered_items': ai,
                'response_vector': rv,
                'parts': ps
            }
        }
        return data


@api.route('/test/statistics')
class Statistics(Resource):
    """
    Obtains some statistics for the student is his/her test.
    """
    def post(self):
        """
        Obtains an approximation of the behavior of the student in the test.
        :return:
        """
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
    """
    Gives the student level according to his/her behaviour.
    """
    def post(self):
        """
        Receives the 3 grades of the student a returns his/her level.
        :return:
        """
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
    
    #_model.train()
    #_model.save_model()
    _model.load_model()
    #print(_model.predict([[2.5, 3.7, 4]]))
    app.run(debug=True, port=5001, host='0.0.0.0', use_reloader=False)
