from __future__ import print_function

import numpy as np
import tflearn
from tflearn.data_utils import load_csv

data, labels = load_csv('testAndGrades.csv', has_header=True, 
target_column=0, categorical_labels=True, n_classes=6)

# Build neural network
net = tflearn.input_data(shape=[None, 3])
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 6, activation='softplus')
net = tflearn.regression(net)

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(data, labels, n_epoch=100, batch_size=16, show_metric=True)

score = model.predict_label([[3,5,5]])
score2 = model.predict([[3,5,5]])
array=score[0]
#print(score2)
print("El estudiante puede aplicar al rango ", array[0])

