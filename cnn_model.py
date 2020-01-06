import glob
import numpy as np

from keras.preprocessing.image import load_img, img_to_array, array_to_img
from keras.preprocessing.image import random_rotation, random_shift, random_zoom
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.layers.core import Flatten
from keras.models import Sequential
from keras.models import model_from_json
from keras.callbacks import LearningRateScheduler
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.utils import np_utils

# 処理共通のパラメータ
FileNames = ["img1.npy", "img2.npy", "img3.npy"]
ClassNames = ["drum", "guiter", "piano"]
hw = {"height": 16, "weight": 16}
directory = "/dataset/reshaped/"


# 前処理
def PreProcess(dirname, filename, var_amount=3):
    num = 0  # 画像ファイルのカウント
    arrlist = []  # 画像ファイルをnumpy型に変換したものを入れるリスト
    files = glob.glob(directory + "*.jpg")

    # 画像処理
    for imgfile in files:
        img = load_img(imgfile, target_size=(
            hw["height"], hw["weight"]))  # 画像ファイルの読み込み
        array = img_to_array(img) / 255  # numpy型データをリストに追加
        arrlist.append(array)
        for i in range(var_amount - 1):
            arr2 = array
            arr2 = random_rotation(arr2, rg=360)
            arrlist.append(arr2)  # numpy型データをリストに追加
        num += 1

    # 保存
    nplist = np.array(arrlist)
    np.save(filename, nplist)
    print(">> " + directory + "から" + str(num) + "個のファイルの読み込み成功")


# モデル構築
def Build(ipshape=(32, 322, 3), num_classes=3):
    model = Sequential()  # 定義

    # 層1
    model.add(Conv2D(24, 3, padding='same', input_shape=ipshape))
    model.add(Activation('relu'))

    # 層2
    model.add(Conv2D(48, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    # 層3,4
    model.add(Conv2D(96, 3, padding='same'))
    model.add(Activation('relu'))

    model.add(Conv2D(96, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    # 層5
    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    # 層6
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    # 構築
    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
    model.compile(loss='categorical_crossentropy',
                  optimizer=adam,
                  metrics=['accuracy'])
    return model
