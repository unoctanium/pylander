# Allow pygame_sdl2 to be imported as pygame.
import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame

import pymunk
from pymunk import Vec2d
import pymunk.pygame_util

import math
import random

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
        random.seed()
        s = world._space_size        

        body = world._space.static_body

        # outer border

        self.static_lines = []
        self.static_lines.append(pymunk.Segment(body, (0, 0), (s[0], 0), 1.0))
        self.static_lines.append(pymunk.Segment(body, (s[0], 0), (s[0], s[1]), 1.0))
        self.static_lines.append(pymunk.Segment(body, (s[0], s[1]), (0, s[1]), 1.0))
        self.static_lines.append(pymunk.Segment(body, (0, s[1]), (0, 0), 1.0))

        # Landscape
        # bottom

        ix = []
        iy = []
        num = random.randrange(20)
        for _ in range(2+num+2):
            ix.append(random.random() * s[0])
            iy.append(random.random() * s[1] * 0.5)
        ix.sort()
        ix[0] = 0
        ix[len(ix)-1] = s[0]

        for i in range(len(ix)-1):
            self.static_lines.append(pymunk.Segment(body, (ix[i], iy[i]), (ix[i+1], iy[i+1]), 1.0))

        # Cave
        # Top

        ix = []
        iy = []
        num = random.randrange(20)
        for _ in range(2+num+2):
            ix.append(random.random() * s[0])
            iy.append(s[1] - random.random() * s[1] * 0.3)
        ix.sort()
        ix[0] = 0
        ix[len(ix)-1] = s[0]

        for i in range(len(ix)-1):
            self.static_lines.append(pymunk.Segment(body, (ix[i], iy[i]), (ix[i+1], iy[i+1]), 1.0))

        #self.static_linesbottom = [pymunk.Segment(body, (0, 10), (s[0]/2, 20.0), 1.0),
        #                pymunk.Segment(body, (s[0]/2,20.0), (s[0],10), 10.0)]
        
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
