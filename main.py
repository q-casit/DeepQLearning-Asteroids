'''
Created on 2018年4月19日

@author: Xie w.
'''

from __future__ import print_function

import tensorflow as tf
import cv2
import sys
sys.path.append("PAdLib/")

import random
import numpy as np
from collections import deque

import pygame
import wrapped_game as wgame
from DQN_Manager import DQN_Manager

# preprocess raw image to 80*80 gray image or, 144*192

img_resize = (144,192) # for cv, (width, height)

def preprocess(observation,img_resize):
    #cv2.resize(image, (100, 50)) ##100 cols (width) and 50 rows (height):
    observation = cv2.cvtColor(cv2.resize(observation, img_resize), cv2.COLOR_BGR2GRAY)
    ret, observation = cv2.threshold(observation,1,255,cv2.THRESH_BINARY)
    return np.reshape(observation,(img_resize[1],img_resize[0],1))


def playAsteroids():
    # Step 1: init BrainDQN
    actions = 5   #always shot
    brain = DQN_Manager(actions)
    
    img_resize = brain.input_dim
    
    ##########
    wgame.load_hs()
    #target_fps = 60
    target_fps = 10
    
    dt = 1.0/float(target_fps)
    wgame.reset_game()

    # Step 3.1: obtain init state, always shot
    action0 = np.array([1,0,0,0,0])  # do nothing
    condit, reward, terminal = wgame.frame_update(dt,action0)
    observation0 = wgame.frame_step()
    
    observation0 = cv2.cvtColor(cv2.resize(observation0, img_resize), cv2.COLOR_BGR2GRAY)    

    ret, observation0 = cv2.threshold(observation0,1,255,cv2.THRESH_BINARY)
    
    brain.setInitState(observation0)
    
    # Step 3.2: run the game
    while 1!= 0:
        action = brain.getAction()
        if not wgame.get_input(dt): break
        condit, reward, terminal = wgame.frame_update(dt,action)     
                
        if not  condit :break
                
        nextObservation = wgame.frame_step()
        
        nextObservation = preprocess(nextObservation,img_resize)
        
        brain.setPerception(nextObservation,action,reward,terminal)
        
        wgame.clock.tick(target_fps)
    
    pygame.quit()

    wgame.write_hs()

    return


def main():
    playAsteroids()

if __name__ == '__main__':
    main()


