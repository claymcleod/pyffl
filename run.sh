#!/bin/bash

# two variables you need to set
pdnndir=/Users/claymcleod/MEGA/DeveloperProjects/Python/pyffl/lib/pdnn  # pointer to PDNN
device=cpu  # the device to be used. set it to "cpu" if you don't have GPUs

# export environment variables
export PYTHONPATH=$PYTHONPATH:$pdnndir
export THEANO_FLAGS=mode=FAST_RUN,device=$device,floatX=float32

# train DNN model
echo "Training the DNN model ..."
python $pdnndir/cmds/run_DNN.py --train-data "train.pickle.gz" \
                                --valid-data "validate.pickle.gz" \
                                --nnet-spec "784:1024:1024:10" --wdir ./ \
                                --l2-reg 0.0001 --lrate "C:0.1:200" --model-save-step 20 \
                                --param-output-file dnn.param --cfg-output-file dnn.cfg
# classification on the testing data; -1 means the final layer, that is, the classification softmax layer
echo "Classifying with the DNN model ..."
python $pdnndir/cmds/run_Extract_Feats.py --data "test.pickle.gz" \
                                          --nnet-param dnn.param --nnet-cfg dnn.cfg \
                                          --output-file "dnn.classify.pickle.gz" --layer-index -1 \
                                          --batch-size 100
