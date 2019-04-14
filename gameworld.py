
import math

class GameWorld():
    
    def __init__(self):
        self._world = (0,0,200,100) # in m
        self._pov = (self._world[2]/2, self._world[3]/2) 
        self._dist = 10.0 # in m
        self._fov2 = (120. / 2.) * (math.pi / 180.) # fov_rad is actually 2 * atan2(device_width_cm / 2, view_dist_cm)
        self._aspr = 10. / 16.
        self._w2 = math.tan(self._fov2) * self._dist
        self._h2 = self._aspr * self._w2

    def setup(self, world, dist, fovdeg, aspx, aspy):
        self._world = world
        self._dist = dist
        self._fov2 = (fovdeg / 2.) * (math.pi / 180.)
        self._aspr = aspy / aspx

    def set_dist(self, dist):
        self._dist = dist
        self._w2 = math.tan(self._fov2) * self._dist

    def set_fov(self, fovdeg):
        self._fov2 = (fovdeg / 2.) * (math.pi / 180.)
        self._w2 = math.tan(self._fov2) * self._dist
    
    def set_aspr(self, aspx, aspy):
        self._aspr = aspy / aspx
        self._h2 = self._aspr * self._w2

    def get_view_from_gwpov(self, pov):
        x = pov[0] - self._w2
        y = pov[1] - self._h2
        return (x, y, self._w2+self._w2, self._h2+self._h2)

    def get_view_from_pxpov(self, pov):
        pass
    

            
    

    