

import math

class GameWorld():

    
    def __init__(self):
        self._world = (0,0,200,100) # in m
        self._pov = (self._world[2]/2, self._world[3]/2) 
        self._dist = 10.0 # in m
        self._fov2 = 60. * (math.pi / 180.)
        self.aspr = (10. / 16.)

    def setup(self, world, dist, fovdeg, aspx, aspy):
        pass
            
    

    