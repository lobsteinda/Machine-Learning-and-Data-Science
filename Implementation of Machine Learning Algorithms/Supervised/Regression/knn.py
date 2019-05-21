import pandas as pd
import numpy as np
import math
import statistics
from sklearn.datasets import load_digits, load_iris, load_boston, load_breast_cancer
from scipy.stats import multivariate_normal as mvn
from sklearn.model_selection import train_test_split
from graphviz import Digraph, Source, Graph
from multiprocessing import cpu_count, Pool
import sklearn
from IPython.display import Math
from sklearn.tree import export_graphviz
from copy import deepcopy
from sklearn.metrics import pairwise_distances


class KNeighbours():
    def __init__(self, k = 5, distance_metric = 'euclid', problem = "classify"):
        self.k = k
        self.distance_metric = distance_metric
        self.problem = problem
        self.prediction_functions = {'classify': self._top_k_votes,
                                     'regress': self._top_k_mean}
        self.eval_functions = {'classify': self._get_accuracy,
                               'regress': self._get_mse}

    def fit(self, X, y):
        self.X = np.asarray(X)
        self.y = np.asarray(y)

    def _euclidien_distance(self, x):
        return np.sqrt(np.sum((x - self.X)**2, axis = 1))

    def _top_k_mean(self, top_k):
        return np.mean(top_k)

    def _top_k_votes(self, top_k):
        return max(top_k, key = list(top_k).count)

    def _get_accuracy(self, pred, y):
        return np.mean((pred == y))

    def _get_mse(self, pred, y):
        return np.mean((pred - y)**2)

    def predict(self, X):
        preds = list()
        X = np.asarray(X)
        for x in X:
            distances = self._euclidien_distance(x)

            # Zip the distances and y values together
            distances = zip(*(distances, self.y))

            # Sort the distances list by distance values in descending order
            distances = sorted(distances, key = lambda x: x[0])

            # Select top k distances
            top_k = distances[:(self.k)]

            top_k = np.array(top_k)
            top_k = top_k[:, 1]

            # Calculate mean of y values of these top k data items
            pred = self.prediction_functions[self.problem](top_k)
            preds.append(pred)

        return preds

    def evaluate(self, pred, y):
        eval_func = self.eval_functions[self.problem]
        return eval_func(pred, y)