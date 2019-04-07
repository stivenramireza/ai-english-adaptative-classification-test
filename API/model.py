import numpy as np
from tflearn import input_data
from tflearn import fully_connected
from tflearn import regression
from tflearn import DNN
from tflearn.data_utils import load_csv

class Model:
    def __init__(self, data=None, labels=None):
        self.data = data
        self.labels = labels
        if(data == None or labels == None):
            self.__load_data()
        self.model = None
        self.MAX_EPOCHS = 30
        self.BATCH_SIZE = 1
        self.model = self.__build_model()
    def __load_data(self, path = './data/testX.csv'):
        self.data, self.labels = load_csv(path, has_header=True, target_column=0, categorical_labels=True, n_classes=6)
        return self.data, self.labels
    def __build_model(self):
        nn = input_data(shape=[None, 3])
        nn = fully_connected(nn, 32)
        nn = fully_connected(nn, 32)
        nn = fully_connected(nn, 6, activation='softplus')
        nn = regression(nn)
        model = DNN(nn)
        return model
    def train(self):
        _data, _labels = self.__load_data()
        _model = self.__build_model()
        _model.fit(_data, _labels, n_epoch=self.MAX_EPOCHS, batch_size=self.BATCH_SIZE, show_metric=True)
        self.model = _model
        return _model
    def save_model(self, path = './nnmodel.tflearn'):
        _model = self.model
        _model.save(path)
        pass
    def load_model(self, path = './nnmodel.tflearn'):
        self.model.load(path)
    def predict(self, scores=[0, 0, 0]):
        return np.array(self.model.predict(scores)).argmax(axis=1)