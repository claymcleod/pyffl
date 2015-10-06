import os
import gzip
import cPickle

from pybrain.structure import *
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

if __name__ == '__main__':
    _dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data/datasets/PlayerVectorizerTransformer")
    model_home_file = gzip.open(os.path.join(_dir, "nn-model-home.pickle.gz"), 'rb')
    net_home = cPickle.load(model_home_file)
    model_away_file = gzip.open(os.path.join(_dir, "nn-model-away.pickle.gz"), 'rb')
    net_away = cPickle.load(model_away_file)
    future_home_file = gzip.open(os.path.join(_dir, "futures_home.pickle.gz"), 'rb')
    futures_home = cPickle.load(future_home_file)
    future_away_file = gzip.open(os.path.join(_dir, "futures_away.pickle.gz"), 'rb')
    futures_away = cPickle.load(future_away_file)

    for (h, a) in zip(futures_home, futures_away):
        home_score = str(int(net_home.activate(h['features'])[0]))
        away_score = str(int(net_away.activate(a['features'])[0]))
        print "%s (%s) - %s (%s)" % (h["name"], home_score, a["name"], away_score)
