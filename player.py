# Allow pygame_sdl2 to be imported as pygame.
import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame

import pymunk
from pymunk import Vec2d

import pymunk.pygame_util

import math

from entity import Entity

class Player(Entity):
    
    body = None
    shape = None
    #space = None
    btnstate = [0,0,0]
    
    #def __init__(self):
    #    Entity.__init__(self)
        
        
    def add(self, space, pos):
        """
        Create a player.
        :return:
        """
        #vs = [(0,0),(0,-45),(25,-45)]
        #shovel_s = pymunk.Poly(chassi_b, vs, transform = pymunk.Transform(tx=85))

        mass = 300
        size = (50,50)
        moment = pymunk.moment_for_box(mass, size)
        hull_b = self.body = pymunk.Body(mass, moment)
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.friction = 0.9
        
        self.shape.elasticity = 0.9
        self.body.position = pos
        space.add(self.body, self.shape)
        #wheel2_s.color = wheel_color
      
        """
        mass = 1
        size = (10,10)
        moment = pymunk.moment_for_box(mass, size)
        mot1_b = pymunk.Body(mass, moment)
        mot1_s = pymunk.Poly.create_box(mot1_b, size)
        mot1_s.friction = 1.5
        mot1_b.position = pos - (25,0)
        space.add(mot1_b, mot1_s)

        mass = 1
        size = (10,10)
        moment = pymunk.moment_for_box(mass, size)
        mot2_b = pymunk.Body(moment, mass)
        mot2_s = pymunk.Poly.create_box(mot2_b, size)
        mot2_s.friction = 1.5
        mot2_b.position = pos + (25,0)
        space.add(mot2_b, mot2_s)
        
        space.add(
            pymunk.PinJoint(mot1_b, hull_b, (0,0), (-25,0)),
            #pymunk.PinJoint(mot1_b, hull_b, (0,0), (-25, 25)),
            #pymunk.PinJoint(mot2_b, hull_b, (0,0), (25,-25)),
            pymunk.PinJoint(mot2_b, hull_b, (0,0), (25, 0))
            )
         """
        
        
          
    def update(self):
        
        if self.btnstate[2] > 0 or (self.btnstate[0] > 0 and self.btnstate[1] > 0):
            self.body.apply_force_at_local_point((0,150000),(0,0))
        elif self.btnstate[0] > 0:
            #self.body.apply_force_at_local_point((-100000,0),(0,0))
            self.body.apply_force_at_local_point((0,20000),(20,-20))
        elif self.btnstate[1] > 0:
            #self.body.apply_force_at_local_point((100000,0),(0,0))                                   
            self.body.apply_force_at_local_point((0,20000),(-20,-20))                                   




    def draw(self, screen):
        
        ps = [pymunk.pygame_util.to_pygame(v.rotated(self.shape.body.angle) + self.shape.body.position, screen) for v in self.shape.get_vertices()]
        ps += [ps[0]]        
        pygame.draw.polygon(screen, pygame.Color(0,255,0), ps)
        pygame.draw.lines(screen, pygame.Color(255,0,0), False, ps, 2)
        
        r = 200
        v = self.body.position
        rot = self.body.rotation_vector
        p = self.transform_physic_screen(v)
        p2 = Vec2d(rot.x, -rot.y) * r 
        p2.rotate(math.pi / -2)
        #screen.set_clip((0,0,800,640))
        pygame.draw.line(screen, pygame.Color(255,0,0), p, p+p2)
        #screen.set_clip(None)
        
    def input(self, btn, state):
        self.btnstate[btn] = state
        
        
        
