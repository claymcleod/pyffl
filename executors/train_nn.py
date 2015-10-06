import os
import gzip
import cPickle

from pybrain.structure import *
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

if __name__ == '__main__':
    _dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data/datasets/PlayerVectorizerTransformer")
    train_home_file = gzip.open(os.path.join(_dir, "train_home.pickle.gz"), 'rb')
    train_away_file = gzip.open(os.path.join(_dir, "train_away.pickle.gz"), 'rb')
    (X_train_home, y_train_home) =  cPickle.load(train_home_file)
    (X_train_away, y_train_away) =  cPickle.load(train_away_file)

    print "Training home NN..."
    ds = SupervisedDataSet(X_train_home.shape[1], 1)
    for (train, test) in zip(X_train_home, y_train_home):
        ds.addSample(tuple(train), (test,))

    net = buildNetwork(X_train_home.shape[1], 22, 1, hiddenclass=LSTMLayer,recurrent=True)
    trainer = BackpropTrainer( net, dataset=ds, verbose=True, momentum=0.9, learningrate=0.0001 )

    trainer.trainUntilConvergence()
    model = gzip.open(os.path.join(_dir, "nn-model-home.pickle.gz"), 'wb')
    cPickle.dump(net, model)

    print "Training away NN..."
    ds_away = SupervisedDataSet(X_train_away.shape[1], 1)
    for (train, test) in zip(X_train_away, y_train_away):
        ds_away.addSample(tuple(train), (test,))

    net = buildNetwork(X_train_away.shape[1], 22, 1, hiddenclass=LSTMLayer,recurrent=True)
    trainer = BackpropTrainer( net, dataset=ds_away, verbose=True, momentum=0.9, learningrate=0.0001 )


    trainer.trainUntilConvergence()
    model = gzip.open(os.path.join(_dir, "nn-model-away.pickle.gz"), 'wb')
    cPickle.dump(net, model)
