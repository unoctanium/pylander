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
    
    #body = None
    shape = None
    #space = None
    btnstate = [0,0,0]
            
    def __init__(self, world, pos):
        """
        Create a player.
        :return:
        """
        #vs = [(0,0),(0,-45),(25,-45)]
        #shovel_s = pymunk.Poly(chassi_b, vs, transform = pymunk.Transform(tx=85))
        Entity.__init__(self)
 
        mass = 300
        size = (5,5)
        moment = pymunk.moment_for_box(mass, size)
        self.body = pymunk.Body(mass, moment)
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.friction = 0.9
        
        self.shape.elasticity = 0.9
        self.body.position = pos
        world._space.add(self.body, self.shape)
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
            self.body.apply_force_at_local_point((0,15000),(0,0))
        elif self.btnstate[0] > 0:
            #self.body.apply_force_at_local_point((-100000,0),(0,0))
            self.body.apply_force_at_local_point((0,2000),(2,-2))
        elif self.btnstate[1] > 0:
            #self.body.apply_force_at_local_point((100000,0),(0,0))                                   
            self.body.apply_force_at_local_point((0,2000),(-2,-2))                                   


    def draw(self, world):
        

        p = self.shape.body.position
        px, py = world.get__space_pov()
        
        if p.x > world._space_viewrect[0] + (world._space_viewrect[2] * 0.75):
            px = p.x - world._space_viewrect[2] * 0.25
            world.set_space_pov((px,py))
        elif p.x < world._space_viewrect[0] + (world._space_viewrect[2] * 0.25):
            px = p.x + world._space_viewrect[2] * 0.25
            world.set_space_pov((px,py))
            
        if p.y > world._space_viewrect[1] + (world._space_viewrect[3] * 0.75):
            py = p.y - world._space_viewrect[3] * 0.25
            world.set_space_pov((px, py))
        elif p.y < world._space_viewrect[1] + (world._space_viewrect[3] * 0.25):
            py = p.y + world._space_viewrect[3] * 0.25
            world.set_space_pov((px, py))



        ps = [world.to_screen(v.rotated(self.shape.body.angle) + self.shape.body.position) for v in self.shape.get_vertices()]
        ps += [ps[0]]
        
        pygame.draw.polygon(world._screen, pygame.Color(0,255,0), ps)
        #pygame.draw.lines(world._screen, pygame.Color(255,0,0), False, ps, 2)
        
        l = 10 # m
        v1 = self.shape.body.position
        v2 = self.shape.body.rotation_vector * l
        v2.rotate(math.pi * -0.5) # neg = clockwise
        v2 += v1
        v1 = world.to_screen(v1)
        v2 = world.to_screen(v2)
        pygame.draw.line(world._screen, pygame.Color(255,0,0), v1, v2)
        
        
    def input(self, btn, state):
        self.btnstate[btn] = state
        
        
        
