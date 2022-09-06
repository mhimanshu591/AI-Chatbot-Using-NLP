# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:42:57 2020

@author: ItsTRD
"""
import tensorflow
import tflearn
import preprocess as bot

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(bot.training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(bot.output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(bot.training, bot.output, n_epoch=1000, batch_size=8, show_metric=True)

model.save("log/model.tflearn")
