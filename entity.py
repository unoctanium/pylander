# Allow pygame_sdl2 to be imported as pygame.
import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame

import pymunk
from pymunk import Vec2d

import pymunk.pygame_util

class Entity():
    pass
    
    #def transform_physic_screen(self, v):
    #    """Small hack to convert chipmunk physics to pygame coordinates"""
    #    return (int (v.x), int(-v.y+pygame.display.Info().current_h))
        
