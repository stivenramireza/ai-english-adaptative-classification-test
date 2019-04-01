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

choices = { 
        0: "El aspirante puede clasificar a los cursos 1, 2 y 3.",
        1: "El aspirante puede clasificar a los cursos 4, 5 y 6.",
        2: "El aspirante puede clasificar a los cursos 7, 8 y 9.", 
        3: "El aspirante puede clasificar a los cursos 10, 11 y 12.", 
        4: "El aspirante puede clasificar a los cursos 13, 14 y 15.",
        5: "El aspirante puede clasificar a los cursos 16, 17 y cursos avanzados.",
        }
print(choices.get(array[0], 'default'))