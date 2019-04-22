from __future__ import print_function

import numpy as np
import tensorflow as tf
import tflearn
from tflearn.data_utils import load_csv

data, labels = load_csv('testX.csv', has_header=True, target_column=0, categorical_labels=True, n_classes=10)
testX, testY = load_csv('testY.csv', has_header=True, target_column=0, categorical_labels=True, n_classes=10)

# Build neural network
net = tflearn.input_data(shape=[None, 3])
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 10, activation='softmax')
net = tflearn.regression(net)

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=200, batch_size=1, show_metric=True)

# Testing model
predicciones = np.array(model.predict(testX)).argmax(axis=1)
correctas = testY.argmax(axis=1)
certeza = np.mean(predicciones == correctas, axis=0)
print("La certeza es de: ", certeza)