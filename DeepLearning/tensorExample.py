import numpy as np
import tensorflow as tf
import tflearn
import tflearn.datasets.mnist as mnist

trainX, trainY, testX, testY = mnist.load_data(one_hot=True)

entradas=784
capa1=128
capa2=128
clases=10

def crear_modelo():
    tf.reset_default_graph()
    red = tflearn.input_data([None, entradas])
    red = tflearn.fully_connected(red, capa1, activation='ReLU')
    red = tflearn.fully_connected(red, capa2, activation='ReLU')
    red = tflearn.fully_connected(red, clases, activation='softmax')
    red = tflearn.regression(red, optimizer='sgd', learning_rate=0.01, loss='categorical_crossentropy')
    modelo = tflearn.DNN(red)
    return modelo

modelo = crear_modelo()

modelo.fit(trainX, trainY, validation_set=0.1, show_metric=True, batch_size=500, n_epoch=100)

predicciones = np.array(modelo.predict(testX)).argmax(axis=1)
correctas = testY.argmax(axis=1)
certeza = np.mean(predicciones == correctas, axis=0)
print("La certeza es de: ", certeza)