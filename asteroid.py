import pygame
import random

from math_helpers import *
import PAdLib.occluder as occluder

class Asteroid:
    speed = 10.0
    
    def __init__(self, position):
        self.position = list(position)
        self.velocity = [
            Asteroid.speed*random.uniform(-1.0,1.0),
            Asteroid.speed*random.uniform(-1.0,1.0)
        ]

        self.angle = random.uniform(0.0,360.0)
        self.spin = random.uniform(-1.0,1.0)

        #self.health = 5
        self.health = 1
        self.radius = 20

        numof_points = random.randint(3,8)
        self.rel_points = []
        for i in range(numof_points):
            angle = (i*2*pi)/numof_points
            point = []
            point.append(  cos(angle)  )
            point.append(  sin(angle)  )
            self.rel_points.append(point)
        
##    def pointtest(self,point):
##        x = point[0]
##        y = point[1]
##        Lines = []
##        index = 0
##        for index in range(len(self.drawpoints)):
##            p0 = self.drawpoints[index]
##            try: p1 = self.drawpoints[index+1]
##            except: p1 = self.drawpoints[0]
##            Lines.append([p0,p1])
##        for l in Lines:
##            p0 = l[0]
##            p1 = l[1]
##            x0 = p0[0]; y0 = p0[1]
##            x1 = p1[0]; y1 = p1[1]
##            test = (y - y0)*(x1 - x0) - (x - x0)*(y1 - y0)
##            if test < 0: return False
##        return True
    
    def hit(self):
        self.health -= 1
        self.radius -= 2
##        self.shrapnel(self.pos)
##        
##    def shrapnel(self,asteroidlocation):
##        radius = self.health+4
##        for iterator in range(0,12):
##            speed = random.random()
##            if speed < 0.5: speed = 0.5
##            speed *= 0.4
##            angle = random.random()*360.0
##            PosB = [(radius*cos(radians(angle))),(radius*sin(radians(angle)))]
##            PosB[0] += asteroidlocation[0]
##            PosB[1] += asteroidlocation[1]
##            Speed = [speed*cos(radians(angle)),speed*sin(radians(angle))]
##            Shrapnel.append([PosB,Speed,0])

    def update(self, dt, screen_size):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        if self.position[0] < 0:
            self.position[0] = 0
            self.velocity[0] *= -1.0
        elif self.position[0] > screen_size[0]:
            self.position[0] = screen_size[0]
            self.velocity[0] *= -1.0
        if self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] *= -1.0
        elif self.position[1] > screen_size[1]:
            self.position[1] = screen_size[1]
            self.velocity[1] *= -1.0

        self.angle = (self.angle+self.spin) % 360.0

        self.real_points = []
        angle_rad = radians(self.angle)
        for x,y in self.rel_points:
            rotated = rotate_point([self.radius*x,self.radius*y],angle_rad)
            self.real_points.append([
                rotated[0] + self.position[0],
                rotated[1] + self.position[1]
            ])

        self.occluder = occluder.Occluder(self.real_points)
        self.occluder.set_bounce(0.1)
            
    def draw(self, surface):
        pygame.draw.aalines(surface,(255,255,255),True,self.real_points)

























