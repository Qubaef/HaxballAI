import numpy as np
import random
import tensorflow as tf
import os
import matplotlib.pyplot as plt

class DQN:

    def __init__(self, state_size, actions_number, print_model):

        self.input_count = state_size
        self.output_count = actions_number
        self.discount_factor = 0.9
        self.epsilon = 1
        self.epsilon_min_val = 0.05
        self.epsilon_decay = 0.9
        self.learning_rate = 0.0001
        self.gamma = 0.95

        self.model = self.define_model(print_model)


    def define_model(self, print_model):
        # Initialization of tensorflow model
        # RandomNormal(mean=0.0, stddev=0.05) sets network to random state (for more efficient learning)

        config = tf.compat.v1.ConfigProto(gpu_options = 
                         tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
        # device_count = {'GPU': 1}
        )
        config.gpu_options.allow_growth = True
        session = tf.compat.v1.Session(config=config)
        tf.compat.v1.keras.backend.set_session(session)

        model = tf.keras.Sequential()
        # model.add(tf.keras.layers.LeakyReLU(input_shape = (self.input_count,)))
        model.add(tf.keras.layers.Dense(16, input_dim = self.input_count, activation = "tanh"))
        model.add(tf.keras.layers.Dense(32))
        # model.add(tf.keras.layers.Dense(64, kernel_initializer = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.05) ))
        model.add(tf.keras.layers.Dense(self.output_count))

        model.compile(loss='Huber', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))

        # save model as model.png
        # os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38\bin\'
        # tf.keras.utils.plot_model(model, to_file='model.png', show_shapes = True, expand_nested = True)

        if (print_model == 1):
            print(model.summary())

        # print available devices
        # print(tf.config.list_physical_devices())

        return model


    def save_weights(self, filename):
        self.model.save_weights(filename)


    def load_weights(self, filename):
        self.model.load_weights(filename)


    # learn model from given batch
    def learn(self, batch):
        for state, action, reward, next_state, done in batch:
            target = self.model.predict(state)

            target[0][action] = reward

            if not done:
                target[0][action] += self.gamma * np.amax(self.model.predict(next_state, batch_size = len(next_state))[0])

            # TODO?
            # self.model.fit_generate(state, target, epochs=1, verbose=0)
            self.model.fit(state, target, epochs = 1, verbose = 0)

        if self.epsilon > self.epsilon_min_val:
            self.epsilon *= self.epsilon_decay

        batch.clear()


    def print_model(self, accuracy):
        data = []
        for i in range(0, accuracy, 1):
            row = []
            for j in range(int(-accuracy / 2) , int(accuracy / 2), 1):
                state = [i / accuracy, j / accuracy,  0.5]
                state = np.reshape(state,[1, len(state)])
                row.append(np.argmax(self.model.predict(state, batch_size = len(state))[0]))
            data.append(row)

        plt.imshow(data, cmap='gray_r', interpolation='nearest')
        plt.xlabel('Player vector')
        plt.ylabel('Player pos')
        plt.colorbar()
        plt.show(block = True)
        plt.clf()


    def save_model(self, accuracy, filepath):
        data = []
        for i in range(0, accuracy, 1):
            row = []
            for j in range(int(-accuracy / 2), int(accuracy / 2), 1):
                state = [i / accuracy, j / accuracy,  0.5]
                state = np.reshape(state,[1, len(state)])
                row.append(np.argmax(self.model.predict(state)[0]))
            data.append(row)

        plt.imshow(data, cmap='gray_r', interpolation='nearest')
        plt.xlabel('Player vector')
        plt.ylabel('Player pos')
        plt.colorbar()
        plt.savefig(filepath + '/' + 'model.png')
        plt.clf()

        file = open(filepath + '/' + 'parameters.txt', 'w')
        print('Epsilon:\t\t', self.epsilon,
              '\nEpsilon decay:\t\t', self.epsilon_decay,
              '\nLearning rate:\t\t', self.learning_rate,
              '\nGamma:\t\t\t', self.gamma,
              '\n\n\nInput size:\t\t', self.input_count,
              '\nOutput size:\t\t', self.output_count,
              file=file)
        file.close()


    def make_move(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.output_count)  # make random move
        else:
            q_values = self.model.predict(state)        # calculate Q values for every possible move for current state using model
            return np.argmax(q_values)