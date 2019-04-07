from catsim.cat import generate_item_bank
from catsim.initialization import RandomInitializer 
from catsim.selection import MaxInfoSelector
from catsim.estimation import HillClimbingEstimator
from catsim.stopping import MaxItemStopper
from catsim.simulation import Simulator
import glob
import pandas as pd
import numpy as np
class CAT:
    def __init__(self, MAX_QUESTIONS = 20):
        self.MAX_QUESTIONS = MAX_QUESTIONS
        self.MAX_RESPONSES = 3
        self.administered_items = np.array([-1] * self.MAX_QUESTIONS).T
        self.response_vector = [False] * self.MAX_QUESTIONS
        self.dataset = None
        self.items = None
        self.load_data()
        self.load_items()
        self.initializer = RandomInitializer()
        self.estimator = HillClimbingEstimator()
        self.stopper = MaxItemStopper(self.MAX_QUESTIONS)
        self.selector = MaxInfoSelector()
        self.cnt = 0
        self.cur_est_theta = 0.5
        self.n_part1 = 0
        self.n_part2 = 0
        self.n_part3 = 0
        self.c_part1 = 0
        self.c_part2 = 0
        self.c_part3 = 0
    def get_dataset_size(self):
        return int(len(self.dataset) / self.MAX_RESPONSES)
    def load_data(self, path = './data/easy_dataset.csv'):
        self.dataset = pd.read_csv(path)
    def set_value(self, next_item, next_response):
        if self.cnt >= self.MAX_QUESTIONS:
            self.cnt = 0
        else:
            self.administered_items[self.cnt] = next_item
            self.response_vector[self.cnt] = next_response
            self.cnt += 1
        return self.administered_items
    def obtain_question(self, n_item):
        question = self.dataset['PREGUNTA'][n_item * 3]
        return question
    def obtain_responses(self, n_item):
        resp1 = self.dataset['TEXTO'][n_item * 3 + 0]
        resp2 = self.dataset['TEXTO'][n_item * 3 + 1]
        resp3 = self.dataset['TEXTO'][n_item * 3 + 2]
        return [[0, 1, 2],[resp1, resp2, resp3]]
    def obtain_correct_option(self, n_item):
        opt1 = self.dataset['OPCION_CORRECTA'][n_item * 3 + 0]
        opt2 = self.dataset['OPCION_CORRECTA'][n_item * 3 + 1]
        opt3 = self.dataset['OPCION_CORRECTA'][n_item * 3 + 2]
        if opt1 == "S":
            return 0
        if opt2 == "S":
            return 1
        return 2
    def set_item_part(self, n_item, cur_response):
        part = int(self.dataset['Parte'][n_item * 3])
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
    def load_items(self):
        sz = int(len(self.dataset) / self.MAX_RESPONSES)
        self.items = np.ones((sz, 1))
        self.items = np.append(self.items, np.unique(self.dataset['Dificultad']).reshape(sz, 1), axis=1)
        self.items = np.append(self.items, np.zeros((sz, 1)), axis=1)
        self.items = np.append(self.items, np.zeros((sz, 1)), axis=1)
        self.items = np.append(self.items, np.zeros((sz, 1)), axis=1)
    def next_item(self, n_item = 0, cur_response=True):
        self.cur_est_theta = self.estimator.estimate(index=n_item, items = self.items, 
                                            administered_items = self.administered_items, 
                                            response_vector = self.response_vector,
                                            est_theta = self.cur_est_theta)
        n_item = self.selector.select(index = n_item, 
                                    administered_items = self.administered_items, 
                                    items = self.items, 
                                    est_theta = self.cur_est_theta)
        print(n_item)
        self.set_value(n_item, cur_response)
        self.set_item_part(n_item, cur_response)
        return n_item
    def ask(self, n_item, n_reponse, first_to_ask=False, cur_est_theta = 0):
        if cur_est_theta != 0:
            self.cur_est_theta = cur_est_theta
        _co = self.obtain_correct_option(n_item)
        _tru_ = (_co == n_reponse)
        n_item = self.next_item(n_item = n_item, cur_response = _tru_)
        question = self.obtain_question(n_item)
        _set_ = self.obtain_responses(n_item)
        responses = _set_[1]
        responses_ids = _set_[0]
        return (n_item, question, responses, responses_ids)
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