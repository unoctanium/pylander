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
    
    body = None
    #shape = None
    static_lines = None
    
    #def __init__(self):
    #    Entity.__init__(self)
            
    def add(self, space):
        """
        Create a Scenery.
        :return:
        """
        w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
        
        self.body = space.static_body
        self.static_lines = [pymunk.Segment(self.body, (0, 100), (w/2, 200.0), 0.0),
                        pymunk.Segment(self.body, (w/2,200.0), (w,0.), 0.0)]
        for line in self.static_lines:
            line.elasticity = 0.9
            line.friction = 0.9
        space.add(self.static_lines)
                  
    def update(self):
        pass        

    def draw(self, screen):
        
        for line in self.static_lines:
            p1 = pymunk.pygame_util.to_pygame(line._get_a(), screen)
            p2 = pymunk.pygame_util.to_pygame(line._get_b(), screen)
            pygame.draw.aalines(screen, pygame.Color(255,255,255), False, [p1,p2])
