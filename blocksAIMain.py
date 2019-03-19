#!/usr/bin/env python3

import sys

from keras.callbacks import TensorBoard

sys.path.append("./utils")
sys.path.append("./ai")
import BlocksEnv
import BlocksProcessor
import StatsCallback
import numpy as np
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten, Activation
from rl.memory import SequentialMemory
from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy


def model():
    m = Sequential()
    m.add(Flatten(input_shape=(1,) + (121, )))
    m.add(Dense(1000, input_dim=121))
    # m.add(Dropout(0.15))
    m.add(Activation('relu'))
    m.add(Dense(1000))
    m.add(Activation('relu'))
    m.add(Dense(1000))
    m.add(Activation('relu'))
    m.add(Dense(1000))
    m.add(Activation('relu'))
    m.add(Dense(1000))
    m.add(Activation('relu'))
    m.add(Dense(192))
    m.add(Activation('sigmoid'))
    # m.add(Dropout(0.15))
    # m.add(Dense(750, activation='relu'))
    # m.add(Dropout(0.15))
    # m.add(Dense(750, activation='relu'))
    # m.add(Dropout(0.15))
    # m.add(Dense(750, activation='relu'))
    # m.add(Dropout(0.15))
    # m.add(Dense(192, activation='linear'))

    print(m.summary())
    return m


def main():
    env = BlocksEnv.BlocksEnv()
    processor = BlocksProcessor.BlocksProcessor()
    np.random.seed(123)
    env.seed(123)
    m = model()
    # tensorBoardCallback = TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=32, write_graph=True,
    #                                   write_grads=False, write_images=False, embeddings_freq=0,
    #                                   embeddings_layer_names=None, embeddings_metadata=None, embeddings_data=None,
    #                                   update_freq='epoch')
    tensorBoardCallback = TensorBoard(log_dir='./logs', update_freq='epoch')
    statsCallback = StatsCallback.StatsCallback()
    memory = SequentialMemory(limit=1000000, window_length=1)
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.01, value_test=.05,
                                  nb_steps=700000)
    dqn = DQNAgent(model=m, nb_actions=(64 * 3), policy=policy, memory=memory,
                   nb_steps_warmup=50000, gamma=.99, target_model_update=10000,
                   processor=processor, train_interval=4, delta_clip=1.)
    dqn.compile(Adam(lr=.00025), metrics=['mae', 'mse', 'acc'])
    dqn.fit(env, nb_steps=1000000, log_interval=10000, callbacks=[tensorBoardCallback, statsCallback])


if __name__ == "__main__":
    main()
