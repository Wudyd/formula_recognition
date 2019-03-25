# encoding:utf-8
# import os
# from PIL import Image
import numpy as np
# import tensorflow as tf
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras import optimizers
from keras import backend as K

# print(tf.__version__)
# dimensions of our images.
img_width, img_height = 100, 100

train_data_dir = './data-training (copy)'
validation_data_dir = './data-testing (copy)'
# test_data_dir = './testset'

# used to rescale the pixel values from [0, 255] to [0, 1] interval
datagen = ImageDataGenerator(rescale=1. / 255)

# automagically retrieve images and their classes for train and validation sets
train_generator = datagen.flow_from_directory(
    train_data_dir,
    color_mode='grayscale',
    target_size=(img_width, img_height),
    batch_size=128,
    class_mode='categorical')

validation_generator = datagen.flow_from_directory(
    validation_data_dir,
    color_mode='grayscale',
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode='categorical')

# test_generator = datagen.flow_from_directory(
#     test_data_dir,
#     target_size=(img_width, img_height))

model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(img_width, img_height, 1),padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))

model.add(Conv2D(32, (3, 3),padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))

model.add(Conv2D(64, (3, 3),padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))

model.add(Flatten())

model.add(Dense(64,activation='relu'))
# model.add(Activation('relu'))

model.add(Dropout(0.5))
model.add(Dense(12,activation='sigmoid'))
# model.add(Activation('sigmoid'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

nb_epoch = 4
steps_per_epoch = 48220 / 128
validation_steps = 864 / 32

model.fit_generator(
    train_generator,
    steps_per_epoch=steps_per_epoch,
    epochs=nb_epoch,
    validation_data=validation_generator,
    validation_steps=validation_steps)


model.save_weights('models/basic_cnn_70_2_epochs.h5')

# from skimage import io, transform
#
# model.load_weights('models/basic_cnn_70_1_epochs.h5')
# img = io.imread("14.74.jpg",as_grey=True)
# img = transform.resize(img, (100, 100,1))
# imges = np.array([img])
#
# print(imges.shape)
# result = model.predict_on_batch(np.array(imges))
# maxv = np.amax(result)
# print(result)
# for i, value in enumerate(result):
#     for index, v2 in enumerate(value):
#         if v2 == maxv:
#             print("This picture is %s" % (index))
#

loss, acc = model.evaluate_generator(validation_generator, validation_steps)
print("loss=%s , accuracy=%s" % (loss, acc))