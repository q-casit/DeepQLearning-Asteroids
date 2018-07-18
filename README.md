# DeepQLearning-Asteroids
Light Deep Q Network Learning in Asteroids game

This is code for Asteroids game (which is a typical vector game) with Deep Q Network Algorithm , a little bit more complexity than FlappyBird. 

The game has 5 action inputs, adopt the basic Deep Q network algorithm from DeepLearningFlappyBird, but rewrite the network layers which has 4 convolution neural network layers inside hidden layers, reshape samples' input size, design batch cache and reward with different action states, etc.

This code could be improved and use multiple Q tables network.

![Alt text](https://github.com/q-casit/DeepQLearning-Asteroids/blob/master/Video_2018-07-02_223638.gif?raw=true "dqn asteroids")

Dependencies:

Python 2.7 or 3,TensorFlow,pygame,OpenCV-Python

How to run:

python main.py

Disclaimer:

This work is based on the repo: yenchenlin1994 DeepLearningFlappyBird,
floodsung DRL-FlappyBird and pygame Asteroids
