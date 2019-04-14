# Allow pygame_sdl2 to be imported as pygame.
import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame

import pymunk
from pymunk import Vec2d
import pymunk.pygame_util

import math

from entity import Entity

class Scenery(Entity):
    
    #body = None
    #shape = None
    static_lines = None
                
    def __init__(self, world):
        """
        Create a Scenery.
        :return:
        """
        Entity.__init__(self)

        s = world._space_size        
        body = world._space.static_body
        self.static_lines = [pymunk.Segment(body, (0, 10), (s[0]/2, 20.0), 0.0),
                        pymunk.Segment(body, (s[0]/2,20.0), (s[0],10), 0.0)]
        for line in self.static_lines:
            line.elasticity = 0.9
            line.friction = 0.9
        world._space.add(self.static_lines)
                  
    def update(self):
        pass        

    def draw(self, world):
        
        for line in self.static_lines:
            p1 = world.to_screen(line._get_a())
            p2 = world.to_screen(line._get_b())
            pygame.draw.aalines(world._screen, pygame.Color(255,255,255), False, [p1,p2])
