# Allow pygame_sdl2 to be imported as pygame.
import pygame_sdl2
pygame_sdl2.import_as_pygame()
import pygame
# Import pymunc physics engine
import pymunk
from pymunk import Vec2d
import pymunk.pygame_util
# Import other libs
#import os
# Import own classes
from eventdispatcher import EventDispatcher
from entity import Entity
from player import Player
from scenery import Scenery
from menu import Menu

class LanderApp:
    def __init__(self, screen_w, screen_h):
        
        #
        # Initialize Screenworld
        #

        # pygame = Screenworld
        pygame.init()

        # DEBUG SCREEN_INFO
        print("INFO")
        print(pygame.display.Info())
        print("MODES")
        print(pygame.display.list_modes(depth=0) )
        print("FULLSCREEN_MODES")
        print(pygame.display.list_modes(depth=0, flags=pygame.FULLSCREEN))

        # set display mode and calculate _screen_size
        if screen_w==0 and screen_h==0:
            self._screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        else:
            self._screen_size = (screen_w, screen_h)
        #self._screen = pygame.display.set_mode(self._screen_size, flags=pygame.FULLSCREEN)
        self._screen = pygame.display.set_mode(self._screen_size)        

        # Frame rate
        self._fps = 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1
        # Time steps
        self._dt = 1.0/self._fps/self._physics_steps_per_frame       
        #self._dt = 1. / self._fps 

        # pygame frame clock
        self._clock = pygame.time.Clock()

        #
        # Initialize Game World
        #

        # Space = GameWorld
        self._space = pymunk.Space()
        # Gravity in m / s^2
        self._space.gravity = (0.0, -9.81)
        # Phyicsworld damoing in 1-x %
        self._space.damping = 0.8
        ## sleep time theshold
        #self.space.sleep_time_threshold = 0.3
        # zoomfactor from physicsworld to pixelworld. 1 = show 100% of space.width on screen, 2=50%
        self._zoom = 2
        # Physicsworld size in m
        self._space_size = (512, 320)
        # Camera POV in space in m from left,down
        self._space_pov = (256, 160)
        
        # Scale factor from space to screen. 1 m in space = <scale> pixel in screen 
        #self._scale = Vec2d(self._screen_size).get_length() / Vec2d(self._space_size).get_length()
        self._scale = self._screen_size[0] / self._space_size[0]
        #print("SCALE: {0:f}".format(self._scale))
        
        # viewrect of current cam in space
        self._space_viewrect = (0,0,0,0)
        self._calc_space_viewrect()

        #
        # Initialize Game Options
        #

        # Drawing Option. Setting _is_is_drawing to False enables headless mode
        self._is_drawing = True

        # Use pymunk debug draw. Note: I can't use it because I implement a scroller, scaler and zoom
        # So I use my own drawing routines in the Entity-Subclasses
        #self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Execution control 
        self._is_running = True
        self._is_paused = True
        self._show_menu = True

        #
        # Create Game Entities
        #
                
        # GUI
        self._font = pygame.font.SysFont("DejaVuSans", 24)
        self._text = self._font.render("Touch the screen.", True, (255, 255, 255, 255))
        self._text_w, self._text_h = self._text.get_size()
        self._add_hud()

        # Menu
        self.menu = Menu()

        # Static Scenery
        self.scenery = Scenery(self)

        # Player
        #self.player = Player(self._space, Vec2d(self._space_size)/2)
        self.player = Player(self, Vec2d(256,160))
        
        # Add Event Dispatcher for user input
        self.ev = EventDispatcher()               
     
            
    def run(self):
        """
        The main loop of the game.
        :return: None
        """
        # Main loop             
        while self._is_running:
           
            self._process_events()
            self._clear_screen()
                    
            if not self._is_paused:
                ## Progress time forward
                #self._space.step(self._dt)
                for x in range(self._physics_steps_per_frame):
                    self._space.step(self._dt)

                self.scenery.update()
                self.player.update()
                self._update_hud()
                
            # Delay fixed time between frames
            self._clock.tick(self._fps)
            #pygame.display.set_caption("fps: " + str(self._clock.get_fps()))
                    
            self._draw_objects()
               
            ### All done, lets flip the display
            pygame.display.flip()
           

    def _process_events(self):
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        # Handle menu
        if self._show_menu:
            menu_choice = self.menu.update(self.menu, self)
            if menu_choice == "Play":
                self._show_menu = False
                self._is_paused = False
			
			#if menu_choice == "Options":
			#	self.option_menu =
			
        if not self._is_paused:
            for event in self.ev.get():
                if event["type"] == self.ev.BTNDN:
                    self.player.input(event["idx"],1)
                elif event["type"]== self.ev.BTNUP:
                    self.player.input(event["idx"],0)
                elif event["type"] == self.ev.QUIT or event["type"] == self.ev.ESCAPE:
                    self._is_running = False
                elif event["type"] == self.ev.DRAW:
                    self._is_drawing = not self._is_drawing
                elif event["type"] == self.ev.ZOOMINC:
                    self.set_zoom(self.get_zoom()*1.05)
                elif event["type"] == self.ev.ZOOMDEC:
                    self.set_zoom(self.get_zoom()*0.95)
                    
                
#                self._text = self._font.render("Finder DOWN: {0:d}, {1:f}, {2:f}".format(f, x, y), True, (255, 255, 255, 255))     
#                self._text = self._font.render("Finder DOWN: {0:d}, {1:d}".format(pygame.display.Info().current_w, pygame.display.Info().current_h), True, (255, 255, 255, 255))   
            
                    
    def _clear_screen(self):
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill((0,0,0,255))


    def _draw_objects(self):
        """
        Draw the objects.
        :return: None
        """
        if self._show_menu:
            self.menu.draw(self._screen)
            
        elif not self._is_paused:
            ### Draw space
            #self._space.debug_draw(self._draw_options)
            self.scenery.draw(self)
            self.player.draw(self)
    
        
    def _add_hud(self):
        pass
            
    def _update_hud(self):
        #fps_str = "fps: " + str(self._clock.get_fps())
        self._screen.blit(self._text, (self._screen_size[0]/2 - self._text_w / 2, self._screen_size[1]/2 - self._text_h / 2))

    def to_screen(self, p):
        z = self._scale * self._zoom
        fx = 0.5 * self._space_size[0] / self._zoom
        fy = 0.5 * self._space_size[1] / self._zoom

        #x = (p[0] - self._space_pov[0]) * z + self._screen_size[0]/2
        x = (p[0] - self._space_pov[0] + fx) * z 
        #y = (p[1] - self._space_pov[1]) * z + self._screen_size[1]/2
        y = (p[1] - self._space_pov[1] + fy) * z
        
        #print("s:{0:f}, z:{1:f}, p0:{2:f}, p1:{3:f}, wp0:{4:f}, wp1:{5:f}".format(world._scale, world._zoom, p[0], p[1], world._space_pov[0], world._space_pov[1]))
        return int(x), int(self._screen_size[1] - y)
        
    
    #def to_space(self):
    #    pass

    #def get_mouse_in_space(self, surface):
    #    pass
    #    """Get position of the mouse pointer in pymunk coordinates.
    #    p = pygame.mouse.get_pos()
    #    return from_pygame(p, surface)"""

    def set_space_pov(self, pos):
        self._space_pov = pos
        self._calc_space_viewrect()

    def get__space_pov(self):
        return self._space_pov

    def _calc_space_viewrect(self):
        w = self._space_size[0] / self._zoom
        h = self._space_size[1] / self._zoom
        x = self._space_pov[0] - 0.5 * w
        y = self._space_pov[1] - 0.5 * h
        self._space_viewrect = (x, y, w, h)

    def get_space_viewrect(self):
        return self._space_viewrect
        
    def get_screen_pov(self):
        return self.to_screen(self._space_pov)

    def set_zoom(self, zoom):
        self._zoom = zoom
        self._calc_space_viewrect()

    def get_zoom(self):
        return self._zoom

    def set_scale(self, scale):
        self._scale = scale

    def get_scale(self):
        return self._scale

def main():
    app = LanderApp(0,0)
    app.run()

if __name__ == '__main__':
    main()







