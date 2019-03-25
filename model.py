# encoding:utf-8
import numpy as np
from PIL import Image
from skimage import io
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.layers import Conv2D, MaxPooling2D

from skimage import transform

class MyModel:
    def __init__(self):
        # dimensions of our images.
        img_width, img_height = 28, 28

        self.model = Sequential()

        self.model.add(Conv2D(32, (3, 3), input_shape=(img_width, img_height, 1),padding='same',activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))

        self.model.add(Conv2D(32, (3, 3),padding='same',activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))

        self.model.add(Conv2D(64, (3, 3),padding='same',activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))

        self.model.add(Flatten())

        self.model.add(Dense(64,activation='relu'))

        self.model.add(Dropout(0.5))
        self.model.add(Dense(12,activation='sigmoid'))

        self.model.load_weights('models/basic_cnn_70_1_epochs.h5')

    def recognize(self,img):
        img = transform.resize(img, (28, 28,1))
        imges = np.array([img])
        result = self.model.predict_on_batch(np.array(imges))
        maxv = np.amax(result)
        for i, value in enumerate(result):
            for index, v2 in enumerate(value):
                if v2 == maxv:
                    if index<10:
                        return str(index)
                    else :
                        if index == 10:
                            return '-'
                        else:
                            return '+'