###############################################################################################
# Goal: script to show the usage of TensorBoard in Keras 
# script source: https://github.com/tgjeon/Keras-Tutorials/blob/master/09_tensorboard.py
############################################################################################### 



###############################################################################################
# --- Imports --- 
###############################################################################################
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.datasets import mnist
# from keras import initializations
from keras import initializers
from keras.utils import np_utils
from keras.callbacks import TensorBoard

###############################################################################################
# --- Hyper parameters --- 
###############################################################################################
batch_size = 128
# nb_epoch = 100
nb_epoch = 10

###############################################################################################
# --- Parameters for MNIST dataset --- 
###############################################################################################
nb_classes = 10

###############################################################################################
# --- Parameters for MLP --- 
###############################################################################################
prob_drop_input = 0.2               # drop probability for dropout @ input layer
prob_drop_hidden = 0.5              # drop probability for dropout @ fc layer

###############################################################################################
# --- Initialize Weights --- 
###############################################################################################
def init_weights(shape, name=None):
    return initializers.RandomNormal()
    # return initializers.normal(shape)
    # return initializers.normal(shape, scale=0.01, name=name)

###############################################################################################
# --- Load MNIST dataset --- 
###############################################################################################
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
Y_Train = np_utils.to_categorical(y_train, nb_classes)
Y_Test = np_utils.to_categorical(y_test, nb_classes)

###############################################################################################
# --- Multilayer Perceptron model --- 
###############################################################################################
model = Sequential()
# model.add(Dense(output_dim=625, input_dim=784, init=init_weights, activation='sigmoid', name='dense1'))
model.add(Dense(output_dim=625, input_dim=784, activation='sigmoid', name='dense1'))
# model.add(Dense(output_dim=625, input_dim=625, init=init_weights, activation='sigmoid', name='dense2'))
model.add(Dense(output_dim=625, input_dim=625, activation='sigmoid', name='dense2'))
model.add(Dropout(prob_drop_input, name='dropout1'))
model.add(Dropout(prob_drop_hidden, name='dropout2'))
# model.add(Dense(output_dim=10, input_dim=625, init=init_weights, activation='softmax', name='dense3'))
model.add(Dense(output_dim=10, input_dim=625, activation='softmax', name='dense3'))
model.compile(optimizer=RMSprop(lr=0.001, rho=0.9), loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

###############################################################################################
# --- Train --- 
###############################################################################################
# history = model.fit(X_train, Y_Train, nb_epoch=nb_epoch, batch_size=batch_size, verbose=1,
#                     callbacks=[TensorBoard(log_dir='./logs/09_tensorboard', histogram_freq=1)])
history = model.fit(X_train, Y_Train, nb_epoch=nb_epoch, batch_size=batch_size, verbose=1, validation_data=(X_test, Y_Test), 
                    callbacks=[TensorBoard(log_dir='./logs/09_tensorboard', histogram_freq=1, write_graph=False, write_grads=True, write_images=True)])
###############################################################################################
# --- Evaluate --- 
###############################################################################################
evaluation = model.evaluate(X_test, Y_Test, verbose=1)
print('Summary: Loss over the test dataset: %.2f, Accuracy: %.2f' % (evaluation[0], evaluation[1]))
