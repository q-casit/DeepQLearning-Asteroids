
import pygame
from pygame.locals import *
import sys, os, traceback
from botocore.vendored.requests.compat import str
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"
import random
from math import *

import asteroid
import player_wrap
from math_helpers import *

import PAdLib.occluder as occluder
import PAdLib.particles as particles

from PAdLib import math_helpers

#######
import cv2

pygame.display.init()
pygame.font.init()

###########
clock = pygame.time.Clock()

screen_size = [640,480]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Asteroids II - The Vector - v.4.0.0 - Ian Mallett - 2013")
surface = pygame.display.set_mode(screen_size)

fonts = {
    16 : pygame.font.SysFont("Times New Roman",16,True),
    32 : pygame.font.SysFont("Times New Roman",32,True)
}

fire_colors = [(255,0,0),(255,255,0),(255,200,0),(255,128,0),(128,0,0),(0,0,0)]

############### 
# shock : if asteroid.health == 0:
emitter_shock = particles.Emitter()
emitter_shock.set_particle_emit_density(0)
emitter_shock.set_particle_emit_angle(0.0,360.0)
emitter_shock.set_particle_emit_speed([50.0,400.0])
emitter_shock.set_particle_emit_life([0.5,1.0])
emitter_shock.set_particle_emit_colors([(255,255,255),(0,0,0)])

emitter_hit = particles.Emitter()
emitter_hit.set_particle_emit_density(0)
emitter_hit.set_particle_emit_angle(0.0,360.0)
emitter_hit.set_particle_emit_speed([100.0,100.0])
emitter_hit.set_particle_emit_life([0.5,1.0])
emitter_hit.set_particle_emit_colors([(255,255,255),(255,255,0),(0,0,255),(0,0,0)])

emitter_die = particles.Emitter()
emitter_die.set_particle_emit_density(0)
emitter_die.set_particle_emit_angle(0.0,360.0)
emitter_die.set_particle_emit_speed([50.0,100.0])
emitter_die.set_particle_emit_life([0.5,2.0])
emitter_die.set_particle_emit_colors(fire_colors)

particle_system = particles.ParticleSystem()

############### 
particle_system.add_emitter(emitter_shock,"shock")
particle_system.add_emitter(emitter_hit,"hit")
particle_system.add_emitter(emitter_die,"die")

level_text_brightness = 0

action_list = []

last_ticks = 0

def load_hs():
    global hs
    try:
        f = open("hs.txt","rb")
        hs = int(f.read())
        f.close()
    except:
        hs = 0
def write_hs():
    f = open("hs.txt","wb")
    f.write(str(hs).encode())
    f.close()

def reset_game():
    global level, player1
    level = 0

    player1 = player_wrap.Player([screen_size[0]/2.0,screen_size[1]/2.0])

    next_level()
def next_level():
    global asteroids, bullets, level, level_text_brightness

    level += 1
    ########
    if level > 10 : level = 10

    player1.level_up(level)

    asteroids = []
    for i in range(4*level):
        asteroids.append(asteroid.Asteroid([
            random.randint(0,screen_size[0]),
            random.randint(0,screen_size[1])
        ]))

    level_text_brightness = 1.0

turning = None
count = 0
def get_input(dt):
    global turning, count
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_F2 and not player1.alive:
                reset_game()

    if player1.alive:
        def reset():
                pass
        def set_pos_rot():
            def get_vec(rel,angle_delta):
                rotated = rotate_point(rel,radians(player1.angle+angle_delta))
                return player1.position[0] + rotated[0], player1.position[1] - rotated[1]

        def set_left():
            global count
            count =  5
        def set_right():
            global count
            count = -5
        if keys_pressed[K_LEFT]:
            player1.angle += 4.0
            if turning == None:
                set_left()
                turning = "left"
        if keys_pressed[K_RIGHT]:
            player1.angle -= 4.0
            if turning == None:
                set_right()
                turning = "right"
        if not keys_pressed[K_LEFT] and not keys_pressed[K_RIGHT]:
            if turning != None:
                if turning == "left":
                    set_right()
                else:
                    set_left()
                turning = None
        if count != 0:
            if count < 0: count += 1
            else:         count -= 1
            if count == 0: reset()
        set_pos_rot()
            
        if keys_pressed[K_UP]:
            player1.velocity[0] += dt*player_wrap.Player.thrust*sin(radians(player1.angle))
            player1.velocity[1] += dt*player_wrap.Player.thrust*cos(radians(player1.angle))

        if not keys_pressed[K_UP]:
            pass
        if keys_pressed[K_DOWN]:
            player1.velocity[0] *= 0.99
            player1.velocity[1] *= 0.99
            
        if keys_pressed[K_LCTRL] or keys_pressed[K_RCTRL] or keys_pressed[K_SPACE] or keys_pressed[K_RETURN] or keys_pressed[K_x] or keys_pressed[K_z]:
            player1.shoot()
        
    return True

def update(dt):
    global level_text_brightness, hs
    
    if len(asteroids) == 0:
        next_level()
        
    for asteroid in asteroids:
        asteroid.update(dt, screen_size)
    player1.update(dt, screen_size)
    if player1.score > hs:
        hs = player1.score

    player1.collide_bullets(asteroids, particle_system, dt)
    player1.collide_asteroids(asteroids, particle_system)

#     emitter_rocket.set_position(player1.position)
##    particle_system.set_particle_occluders([asteroid.occluder for asteroid in asteroids])
    particle_system.update(dt)

    if level_text_brightness > 0.0:
        level_text_brightness -= dt

    return True

def draw():
    surface.fill((0,0,0))

    particle_system.draw(surface)

    player1.draw(surface)

    for asteroid in asteroids:
        asteroid.draw(surface)

    ######### 
#     surf_level = fonts[16].render("Level: "+str(level), True, (255,255,255))
#     surface.blit(surf_level,(10,10))
# 
#     surf_lives = fonts[16].render("Lives: "+str(max([player1.lives,0])), True, (255,255,255))
#     surface.blit(surf_lives,(10,25))
#         
#     surf_score = fonts[16].render("Score: "+str(player1.score), True, (255,255,255))
#     surface.blit(surf_score,(screen_size[0]-surf_score.get_width()-10,10))
#     
#     surf_highscore = fonts[16].render("High Score: "+str(hs), True, (255,255,255))
#     surface.blit(surf_highscore,(screen_size[0]-surf_highscore.get_width()-10,25))



    if player1.lives >= 0:
        surf_remain = fonts[16].render("Asteroids Left: "+str(len(asteroids)), True, (255,255,255))
        surface.blit(surf_remain,(10,screen_size[1]-surf_remain.get_height()-10))
    
        if level_text_brightness > 0.0:
            col = rndint(255.0*level_text_brightness)
            surf_level = fonts[32].render("Level "+str(level), True, (col,col,col),(0,0,0))
            pos = [
                (screen_size[0]/2.0)-(surf_level.get_width()/2.0),
                (screen_size[1]/2.0)-(surf_level.get_height()/2.0)
            ]
            surface.blit(surf_level,pos,special_flags=BLEND_MAX)
    else:
        surf_level = fonts[32].render("F2 Starts New Game", True, (255,255,255),(0,0,0))
        pos = [
            (screen_size[0]/2.0)-(surf_level.get_width()/2.0),
            (screen_size[1]/2.0)-(surf_level.get_height()/2.0)
        ]
        surface.blit(surf_level,pos,special_flags=BLEND_MAX)

    image_data = pygame.surfarray.array3d(pygame.display.get_surface())    
    
    pygame.display.flip()
    
    return image_data

###########
from collections import deque
from glob import glob

SAVE_IMG_MEMORY = 16
Dq = deque() 

def saveLastIndexImg(filename):
    
    if len(Dq) < SAVE_IMG_MEMORY:
        Dq.append(filename)
        return
    
    if len(Dq) > SAVE_IMG_MEMORY:
        Dq.popleft()
        Dq.append(len(Dq))
        return
        
    
    image_tmp   = Dq.index(0)
    
    pass

def from_first_4chars(x):
    first_str = './save_img/saveimg_'
    index = len(first_str) -1
    x_len = len(x)
    return(x[ index : x_len-1])

def sortKeyFunc(s):
    first_str = 'saveimg_'
    f_index = len(first_str) 
    basename_t = os.path.basename(s)
    basename_index = len(basename_t)  
    return basename_t[ f_index : basename_index]
    
def saveLastIndexImg2(filename):
    
    exist_files = glob('./save_img/sav*.jpg')
    
    #sort filename from  small to large 
    sorted(exist_files,key=sortKeyFunc)
    print('exist_files: ',exist_files)
    
    
    if len(exist_files) > SAVE_IMG_MEMORY:
        f_left = exist_files[0]
        #f_left = Dq_t.pop()
        
        print('f_left: ',f_left)
        os.remove(f_left)
        
        return  
    
    pass

########################

def get_player_aster_Radian(headAngle,headPosition,aster_pos):
    
    angle_rad = radians(-headAngle+90)
    
    player_head_v = [0,0]
    player_head_v[0] = cos(angle_rad)
    player_head_v[1] = sin(angle_rad)

    player_to_aster_v = math_helpers.vec_sub(aster_pos,headPosition)
    player_to_aster_v = math_helpers.vec_norm(player_to_aster_v)
    
    radian_pToa_phead = math_helpers.angle_radian(player_head_v, player_to_aster_v)
    return radian_pToa_phead
    
    
def getMinAngel_AToP(player,asteroids):
    
    min_angle_rad = 3.1415
    for idx, asteroid in enumerate(asteroids):
        
        ### 0 -> pi
        angle_rad = get_player_aster_Radian(player.angle,player.position, asteroid.position)
        if min_angle_rad > angle_rad:
            min_angle_rad = angle_rad;
            
    ### 0 -> pi        
    return min_angle_rad
    
def getRewardForHeading(player,asteroids):
    min_angle_rad =  getMinAngel_AToP(player,asteroids)
    #print('min_angle_rad: ',min_angle_rad)
    reward = (3.1416 - min_angle_rad) / 10.0
    
    #give more reward when face object
    if min_angle_rad<1:
        reward+=6.0
    elif min_angle_rad>2:
        reward-=6.0
    
    return reward
   
    
##############
def slowdownVelocity(slow_factor, velocity):
    velocity =  math_helpers.vec_scale(slow_factor, velocity)
    return  velocity
    
    
def get_input_action(dt,input_actions):
    global turning, count
    
    reward = 0.02

    if player1.alive:
        def reset():
                pass
        def set_pos_rot():
            def get_vec(rel,angle_delta):
                rotated = rotate_point(rel,radians(player1.angle+angle_delta))
                return player1.position[0] + rotated[0], player1.position[1] - rotated[1]

        def set_left():
            global count
            count =  5
        def set_right():
            global count
            count = -5
            
        if input_actions[1] == 1:
            player1.angle += 4.0
            if turning == None:
                set_left()
                turning = "left"
            player1.velocity = slowdownVelocity(0.5,player1.velocity)
            reward = getRewardForHeading(player1,asteroids)    
            
        if input_actions[2] == 1:
            player1.angle -= 4.0
            if turning == None:
                set_right()
                turning = "right"
            player1.velocity = slowdownVelocity(0.5,player1.velocity)
            reward = getRewardForHeading(player1,asteroids)
            
                
        if  input_actions[1] == 0 and input_actions[2] == 0:
            if turning != None:
                if turning == "left":
                    set_right()
                else:
                    set_left()
                turning = None
        if count != 0:
            if count < 0: count += 1
            else:         count -= 1
            if count == 0: reset()
        set_pos_rot()
            
        # forward
        if input_actions[3] == 1:
            player1.velocity[0] += dt*player_wrap.Player.thrust*sin(radians(player1.angle))
            player1.velocity[1] += dt*player_wrap.Player.thrust*cos(radians(player1.angle))
            reward = 0.25
            
            short_dist_aster = 80000
            short_dist_aster2 = 1000 
            dist_aster_prev = 0
            for idx, asteroid in enumerate(asteroids):
                distance_sq =  math_helpers.point_square_distance(player1.position, asteroid.position)
                if dist_aster_prev == 0:
                    dist_aster_prev = distance_sq
                
                if dist_aster_prev > distance_sq:
                    dist_aster_prev = distance_sq  
                
            ### large dist 90397*2
            if dist_aster_prev <  short_dist_aster and  dist_aster_prev> short_dist_aster2:
                reward+=  (short_dist_aster - dist_aster_prev)/160000
            elif   dist_aster_prev > 0 and   dist_aster_prev < short_dist_aster2:
                reward-= (short_dist_aster2 - dist_aster_prev)/160000

        if input_actions[3] == 0:
            pass
        
        #backward
        if input_actions[4] == 1:
            player1.velocity[0] *= 0.16 #0.99
            player1.velocity[1] *= 0.16 #0.99
            
            reward = 0.01
            if math_helpers.vec_length(player1.velocity) > player_wrap.Player.thrust *5:
                reward = 0.1
            
        ###always shoot
#         if input_actions[5] == 1:           
#             reward = 0.1        
#             player1.shoot()
        
        ticks = pygame.time.get_ticks()
        global last_ticks
        
        if ticks - last_ticks > 320: #if ticks%200 == 0:
            last_ticks = ticks
            player1.shoot()
        
    return True,reward


#######################

def frame_update(dt,input_actions):
    global level_text_brightness, hs
    
    if len(asteroids) == 0:
        next_level()
        
    for asteroid in asteroids:
        asteroid.update(dt, screen_size)
    player1.update(dt, screen_size)
    if player1.score > hs:
        hs = player1.score
        
    ######### input action ---------------
    if sum(input_actions) != 1:
        raise ValueError('Multiple input actions!')        
    
    rt,reward0 = get_input_action(dt,input_actions)
    
    ################## actions store 
    prev_actions_len = 512
    if len(action_list) > prev_actions_len:
        #action_list= action_list[-2:]
        action_list.pop(0)
    
    action_list.append(input_actions)
    
    if len(action_list)>0:
        action_last  = action_list[len(action_list)-1]
        
        count_a = 0
        for action_t in action_list[:-1]:
            if list(action_last) == list(action_t):
                count_a+=1
                #print('action_last== action_t',action_last,action_t)
            else:
                #print('action_last!= action_t',action_last,action_t)
                pass
        
        # if same actions for loop, reduce reward
        if count_a>12:
            reward0 = reward0 - count_a * 0.05
        
        
    ######### get reward ----------------
    reward1 = player1.collide_bullets(asteroids, particle_system, dt)
    reward2,terminal = player1.collide_asteroids(asteroids, particle_system)

    reward = reward1 + reward2  + reward0

    particle_system.update(dt)

    if level_text_brightness > 0.0:
        level_text_brightness -= dt

    return True,reward,terminal

######### equal => draw
def frame_step():

    surface.fill((0,0,0))

    particle_system.draw(surface)

    player1.draw(surface)
    

    for asteroid in asteroids:
        asteroid.draw(surface)
        
    
    image_data = pygame.surfarray.array3d(pygame.display.get_surface()) 

    pygame.display.flip()
    
    return image_data











