# -*- coding: utf-8 -*-
"""Kaggle1_ML2022.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wqVtv45QvJfbkcgHMH2HcG0BaiUyuD8a
"""

from google.colab import drive
drive.mount('/content/gdrive')

import os
os.chdir('/content/gdrive/MyDrive/Kaggle Competition 1/')

import pandas as pd
import scipy.sparse as sp
import numpy as np

train_df = pd.read_csv("Data/train.csv")

train_df = train_df.dropna(1)

test_df = pd.read_csv("Data/test.csv")

test_df = test_df.dropna(1)

train_result_df = pd.read_csv("Data/train_result.csv")

train_result_df = train_result_df.drop(columns = 'Index')

train_result_df = train_result_df.dropna(1)

test = test_df.to_numpy()

train = train_df.to_numpy()

train_new = train[0:20000, :]

test_new = train[40000:, :]

train_result = train_result_df.to_numpy()

pred = train_result[40000:]

train_result_new = train_result[0:20000]

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from scipy.special import softmax
onehot_encoder = OneHotEncoder(sparse=False)
from sklearn.datasets import load_iris

def loss(X, Y, W):
    """
    Y: onehot encoded
    """
    Z = - X @ W
    N = X.shape[0]
    loss = 1/N * (np.trace(X @ W @ Y.T) + np.sum(np.log(np.sum(np.exp(Z), axis=1))))
    return loss

def gradient(X, Y, W, mu):
    """
    Y: onehot encoded 
    """
    Z = - X @ W
    P = softmax(Z, axis=1)
    N = X.shape[0]
    gd = 1/N * (X.T @ (Y - P)) + 2 * mu * W
    return gd

def gradient_descent(X, Y, max_iter=1000, eta=0.1, mu=0.01):
    """
    Very basic gradient descent algorithm with fixed eta and mu
    """
    Y_onehot = onehot_encoder.fit_transform(Y.reshape(-1,1))
    W = np.zeros((X.shape[1], Y_onehot.shape[1]))
    step = 0
    step_lst = [] 
    loss_lst = []
    W_lst = []
 
    while step < max_iter:
        step += 1
        W -= eta * gradient(X, Y_onehot, W, mu)
        step_lst.append(step)
        W_lst.append(W)
        loss_lst.append(loss(X, Y_onehot, W))

    df = pd.DataFrame({
        'step': step_lst, 
        'loss': loss_lst
    })
    return df, W

class Multiclass:
    def fit(self, X, Y):
        self.loss_steps, self.W = gradient_descent(X, Y)

    def loss_plot(self):
        return self.loss_steps.plot(
            x='step', 
            y='loss',
            xlabel='step',
            ylabel='loss'
        )

    def predict(self, H):
        Z = - H @ self.W
        P = softmax(Z, axis=1)
        return np.argmax(P, axis=1)

model = Multiclass()
# model.fit(train_new, train_result_new)
model.fit(train, train_result)
model.loss_plot()

x = model.predict(train_new) == train_result_new.T

test_res_1 = model.predict(test)

# test_res_1



indices = np.array(range(test.shape[0])).T

final = np.vstack((indices, test_res_1))
# final

test_res_1_df = pd.DataFrame(final.T)
test_res_1_df = test_res_1_df.rename({'0': 'Index', '1': 'Class'}, axis=1)
x = test_res_1_df.to_csv('predict.csv')

