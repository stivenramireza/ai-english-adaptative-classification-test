from catsim.initialization import RandomInitializer
from catsim.selection import UrrySelector
from catsim.estimation import DifferentialEvolutionEstimator
from catsim.stopping import MaxItemStopper
import pandas as pd
import numpy as np
class CAT:
    def __init__(self, MAX_QUESTIONS = 20):
        self.MAX_QUESTIONS = MAX_QUESTIONS
        self.MAX_RESPONSES = 3
        #self.administered_items = np.array([-1] * self.MAX_QUESTIONS).T
        #self.response_vector = [False] * self.MAX_QUESTIONS
        self.administered_items = []
        self.response_vector = []
        self.dataset = None
        self.items = None
        self.load_data()
        self.load_items()
        self.initializer = RandomInitializer()
        self.estimator = DifferentialEvolutionEstimator((min(self.items[:,1]), max(self.items[:, 1])))
        self.stopper = MaxItemStopper(self.MAX_QUESTIONS)
        self.selector = UrrySelector()
        self.cnt = 0
        self.cur_est_theta = None
        self.n_part1 = 0
        self.n_part2 = 0
        self.n_part3 = 0
        self.c_part1 = 0
        self.c_part2 = 0
        self.c_part3 = 0
        self.parts = []
    def get_dataset_size(self):
        return int(len(self.dataset) / self.MAX_RESPONSES)
    def load_data(self, path1 = './data/easy_dataset_1.csv', path2 = './data/easy_dataset.csv'):
        self.dataset = pd.read_csv(path1)
        self.dataset1 = pd.read_csv(path2)
    def set_value(self, next_item, next_response, administered_items=None, response_vector=None):
        if len(administered_items) + 1 >= self.MAX_QUESTIONS:
            return None, None
        else:
            """
            for _ in range(self.cnt, self.MAX_QUESTIONS):
                if self.administered_items[_] == -1:
                    self.administered_items[_] = next_item
                    self.response_vector[_] = next_response
            self.administered_items[self.cnt] = next_item
            self.response_vector[self.cnt] = next_response
            self.cnt += 1
            """
            administered_items.append(next_item)
            response_vector.append(next_response)
            #self.cnt += 1
        return administered_items, response_vector
    def obtain_question(self, n_item):
        question = self.dataset1['PREGUNTA'][n_item * 3]
        return question
    def obtain_responses(self, n_item):
        resp1 = self.dataset1['TEXTO'][n_item * 3 + 0]
        resp2 = self.dataset1['TEXTO'][n_item * 3 + 1]
        resp3 = self.dataset1['TEXTO'][n_item * 3 + 2]
        """
        print("Resp 1: " + str(self.dataset['OPCION_CORRECTA'][n_item * 3]))
        print("Resp 2: " + str(self.dataset['OPCION_CORRECTA'][n_item * 3 + 1]))
        print("Resp 3: " + str(self.dataset['OPCION_CORRECTA'][n_item * 3 + 2]))
        """
        return [[0, 1, 2],[resp1, resp2, resp3]]
    def obtain_correct_option(self, n_item):
        opt1 = self.dataset1['OPCION_CORRECTA'][n_item * 3 + 0]
        opt2 = self.dataset1['OPCION_CORRECTA'][n_item * 3 + 1]
        opt3 = self.dataset1['OPCION_CORRECTA'][n_item * 3 + 2]
        if opt1 == "S":
            return 0
        if opt2 == "S":
            return 1
        return 2
    def get_item_part(self, n_item):
        part = int(self.dataset1['Parte'][n_item * 3])
        return part
    def set_item_part(self, n_item, cur_response, parts=None):
        part = int(self.dataset1['Parte'][n_item * 3])
        parts.append(part)
        return parts
        """
        if part == 1:
            self.n_part1 += 1
            if cur_response == True:
                self.c_part1 += 1
        elif part == 2:
            self.n_part2 += 1
            if cur_response == True:
                self.c_part2 += 1
        else:
            self.n_part3 += 1
            if cur_response == True:
                self.c_part3 += 1
        """
    def load_items(self):
        #sz = int(len(self.dataset) / self.MAX_RESPONSES)
        sz = len(self.dataset)
        self.items = np.ones((sz, 1))
        self.items = np.append(self.items, np.unique(self.dataset['Dificultad']).reshape(sz, 1), axis=1)
        self.items = np.append(self.items, np.zeros((sz, 1)), axis=1)
        self.items = np.append(self.items, np.zeros((sz, 1)), axis=1)
        #self.items = np.append(self.items, np.zeros((sz, 1)), axis=1)
    def next_item(self, n_item = -1, cur_response=None):
        if n_item != -1 and cur_response != None:
            self.administered_items.append(n_item)
            self.response_vector.append(cur_response)
            self.parts.append(self.get_item_part(n_item))
        print((self.administered_items, self.response_vector))
        self.cur_est_theta = self.estimator.estimate(items = self.items,
                                            administered_items = self.administered_items, 
                                            response_vector = self.response_vector,
                                            est_theta = self.cur_est_theta)
        n_item = self.selector.select(administered_items = self.administered_items, 
                                    items = self.items, 
                                    est_theta = self.cur_est_theta)
        return n_item
    def set_current_test_status(self, ai, rv, ps, n_item, n_response):
        _co = self.obtain_correct_option(n_item)
        _tru_ = (_co == n_response)
        _ai = self.get_int_array(ai)
        _rv = self.get_boolean_array(rv)
        _ps = self.get_int_array(ps)
        _ai, _rv = self.set_value(n_item, _tru_, _ai, _rv)
        _ps = self.set_item_part(n_item, n_response, _ps)
        self.administered_items = _ai
        self.response_vector = _rv
        self.parts = _ps
    def ask(self, n_item=-1, n_reponse=None, cur_est_theta = None):
        if cur_est_theta != None:
            self.cur_est_theta = cur_est_theta
        nn_item = 0
        _tru_ = False
        if n_item != -1 and n_reponse != None:
            _co = self.obtain_correct_option(n_item)
            _tru_ = (_co == n_reponse)
            nn_item = self.next_item(n_item = n_item, cur_response = _tru_)
        else:
            nn_item = self.next_item()
        question = self.obtain_question(nn_item)
        _set_ = self.obtain_responses(nn_item)
        responses = _set_[1]
        responses_ids = _set_[0]
        return ( 
            _tru_, 
            nn_item,
            question, 
            responses,
            responses_ids
            )
    def get_current_test_status(self):
        return (
            self.cur_est_theta,
            self.administered_items[0:],
            self.response_vector[0:],
            self.parts[0:]
        )
    def get_statistics(self):
        _, __, ___ = 0, 0, 0
        if self.n_part1 == 0:
            _ = 0
        else:
            _ = 1.0 * self.c_part1 / self.n_part1
        if self.n_part2 == 0:
            __ = 0
        else:
            __ = 1.0 * self.c_part2 / self.n_part2
        if self.n_part3 == 0:
            ___ = 0
        else:
            ___ = 1.0 * self.c_part3 / self.n_part3
        return [_, __, ___]
    def get_boolean_array(self, _):
        treat = []
        for x in list(_):
            treat.append(bool(x))
        return treat
    def get_int_array(self, _):
        treat = []
        for x in list(_):
            treat.append(int(x))
        return treat