from __future__ import print_function

import numpy as np
import tflearn
from tflearn.data_utils import load_csv

data, labels = load_csv('testAndGrades.csv', has_header=True, target_column=0, categorical_labels=True, n_classes=16)

# Build neural network
net = tflearn.input_data(shape=[None, 3])
net = tflearn.fully_connected(net, 15)
net = tflearn.fully_connected(net, 15)
net = tflearn.fully_connected(net, 16, activation='softmax')
net = tflearn.regression(net)

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=400, batch_size=1, validation_batch_size=3, show_metric=True)

