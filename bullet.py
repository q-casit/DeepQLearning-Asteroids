from math_helpers import *

class Bullet(object):
    speed = 320.0  # 500
    
    def __init__(self, position,angle_rad):
        self.position = list(position)
        self.velocity = [
            Bullet.speed * cos(angle_rad),
            Bullet.speed * sin(angle_rad)
        ]

        self.time = 0.0

    def update(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

        self.time += dt

    def draw(self, surface):
        x,y = rndint(self.position[0]),rndint(self.position[1])
        surface.set_at( (x,y), (200,200,255) )
        surface.set_at( (x-1,y), (200,200,255) )
        surface.set_at( (x+1,y), (200,200,255) )
        surface.set_at( (x,y-1), (200,200,255) )
        surface.set_at( (x,y+1), (200,200,255) )
