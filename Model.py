import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from tensorflow.keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.utils import to_categorical, plot_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow.keras.backend as K

# Load dataset
data = pd.read_csv("data.csv")
dataset = np.array(data)
np.random.shuffle(dataset)
X = dataset
Y = dataset
X = X[:, 0:1024]
Y = Y[:, 1024]

# Split the dataset into train and test
X_train = X[0:70000, :]
X_train = X_train / 255.0
X_test = X[70000:72001, :]
X_test = X_test / 255.0

# Reshape the labels
Y = Y.reshape(Y.shape[0], 1)
Y_train = Y[0:70000, :]
Y_train = Y_train.T
Y_test = Y[70000:72001, :]
Y_test = Y_test.T

# Print dataset information
print("number of training examples = " + str(X_train.shape[0]))
print("number of test examples = " + str(X_test.shape[0]))
print("X_train shape: " + str(X_train.shape))
print("Y_train shape: " + str(Y_train.shape))
print("X_test shape: " + str(X_test.shape))
print("Y_test shape: " + str(Y_test.shape))

# Image dimensions
image_x = 32
image_y = 32

# One-hot encode the labels
train_y = to_categorical(Y_train)
test_y = to_categorical(Y_test)

# Reshape the one-hot encoded labels and input images
train_y = train_y.reshape(train_y.shape[1], train_y.shape[2])
test_y = test_y.reshape(test_y.shape[1], test_y.shape[2])
X_train = X_train.reshape(X_train.shape[0], image_x, image_y, 1)
X_test = X_test.reshape(X_test.shape[0], image_x, image_y, 1)

print("X_train shape: " + str(X_train.shape))
print("Y_train shape: " + str(train_y.shape))

# Define the CNN model
def keras_model(image_x, image_y):
    num_of_classes = 37
    model = Sequential()
    model.add(Conv2D(filters=32, kernel_size=(5, 5), input_shape=(image_x, image_y, 1), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    model.add(Conv2D(64, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(5, 5), strides=(5, 5), padding='same'))
    model.add(Flatten())
    model.add(Dense(num_of_classes, activation='softmax'))
    
    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    # Model checkpoint callback
    filepath = "devanagari.keras"
    checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]
    
    return model, callbacks_list

# Build and train the model
model, callbacks_list = keras_model(image_x, image_y)
model.fit(X_train, train_y, validation_data=(X_test, test_y), epochs=8, batch_size=64, callbacks=callbacks_list)

# Evaluate the model
scores = model.evaluate(X_test, test_y, verbose=0)
print("CNN Error: %.2f%%" % (100 - scores[1] * 100))

# Print the model summary
model.summary()

# Save the model
model.save('devanagari.keras')
