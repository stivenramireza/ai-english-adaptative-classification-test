import numpy as np
from tflearn import input_data
from tflearn import fully_connected
from tflearn import regression
from tflearn import DNN
from tflearn.data_utils import load_csv
import tensorflow as tf
class Model:
    """
        Model for creating adaptative tests according to Centro de Idiomas rules.
    """
    def __init__(self, data=None, labels=None):
        """
        Initializes the model
        :param data: Model data which is composed of different grades of the students.
        :param labels: Model labels which is compose of all labels for the model.
        """
        self.data = data
        self.labels = labels
        if(data == None or labels == None):
            self.__load_data()
        self.model = None
        self.MAX_EPOCHS = 200
        self.BATCH_SIZE = 16
        self.model = self.__build_model()
    def __load_data(self, path = './data/testAndGrades.csv'):
        """
        Loads the data for the model.
        :param path: Path to the data of the model. It should be a csv file.
        :return: A pandas csv with all the data for the model to train.
        """
        self.data, self.labels = load_csv(path, has_header=True, target_column=0, categorical_labels=True, n_classes=10)
        return self.data, self.labels
    def __build_model(self):
        """
        Composes a neural network architecture capable of predicting the level of a student given his/her grades.
        :return: The neural network model.
        """
        tf.compat.v1.reset_default_graph()
        nn = input_data(shape=[None, 3])
        nn = fully_connected(nn, 32)
        nn = fully_connected(nn, 32)
        nn = fully_connected(nn, 10, activation='softmax')
        nn = regression(nn)
        model = DNN(nn)
        return model
    def train(self):
        """
        Trains the neural network with the parameters passed in the initialization.
        :return: The neural network model.
        """
        _data, _labels = self.__load_data()
        _model = self.__build_model()
        _model.fit(_data, _labels, n_epoch=self.MAX_EPOCHS, batch_size=self.BATCH_SIZE, show_metric=True)
        self.model = _model
        return _model
    def save_model(self, path = './nnmodel.tflearn'):
        """
        Saves a model checkpoint to avoid unnecessary training in the future.
        :param path:
        :return:
        """
        _model = self.model
        _model.save(path)
        pass
    def load_model(self, path = './nnmodel.tflearn'):
        """
        Loads the model from an specified checkpoint.
        :param path: Path to the checkpoint
        :return:
        """
        self.model.load(path)
    def predict(self, scores=[0, 0, 0]):
        """
        Returns a student level given his/her grades.
        :param scores: Grades of a student.
        :return: The level of the student. It's a number from 0-9. 0: Lowest level. 9: Highest level.
        """
        return np.array(self.model.predict(scores)).argmax(axis=1)