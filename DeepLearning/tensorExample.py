from __future__ import print_function

import numpy as np
import tflearn
from tflearn.data_utils import load_csv
import csv

data, labels = load_csv('testAndGrades.csv', has_header=True, 
target_column=0, categorical_labels=True, n_classes=10)

# Construcción de la red neuronal. Definiendo 3 entradas y 10 posibles salidas
net = tflearn.input_data(shape=[None, 3])
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 10, activation='softmax')
net = tflearn.regression(net)

# Definición del modelo
model = tflearn.DNN(net)
# Inicio del entrenamiento del modelo
model.fit(data, labels, n_epoch=200, batch_size=16, show_metric=True)

#Prueba del modelo
print("Prueba en tiempo real")
calificacionFac = input("Ingrese la calificacion del estudiante en las preguntas de nivel facil: ")
calificacionMed = input("Ingrese la calificacion del estudiante en las preguntas de nivel intermedio: ")
calificacionDif = input("Ingrese la calificacion del estudiante en las preguntas de nivel avanzado: ")
score = model.predict_label([[calificacionFac,calificacionMed,calificacionDif]])
array=score[0]

choices = { 
        0: "El aspirante puede clasificar al curso de principiantes .",
        1: "El aspirante puede clasificar a los cursos 1 y 2.",
        2: "El aspirante puede clasificar a los cursos 3 y 4.", 
        3: "El aspirante puede clasificar a los cursos 5 y 6.", 
        4: "El aspirante puede clasificar a los cursos 7 y 8.",
        5: "El aspirante puede clasificar a los cursos 9 y 10.",
        6: "El aspirante puede clasificar a los cursos 11 y 12.",
        7: "El aspirante puede clasificar a los cursos 13 y 14.",
        8: "El aspirante puede clasificar a los cursos 15 y 16.",
        9: "El aspirante puede clasificar al curso 17 y a cursos avanzados.",
        }
print(choices.get(array[0], 'default'))
print("")


print("Realizando pruebas en lotes, utilizando el archivo de entrada test.csv")
with open("test.csv") as f:
    reader = csv.reader(f, delimiter=",")
    count = 0
    correctas = 0
    for row in reader:
        print("se espera: ",row[0])
        score = model.predict_label([[row[1],row[2],row[3]]])
        array = score[0]
        print("Se obtuvo: " ,array[0])
        if (int(array[0]) == int(row[0])):
            correctas = correctas + 1
        count = count + 1
        print (count, " iteración.")
        print("----")
    print (count, " Registros probados.")
    print (correctas, " Pruebas correctas.")