# Allow pygame_sdl2 to be imported as pygame.
import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
#import os

import pymunk
from pymunk import Vec2d
import pymunk.pygame_util

from eventdispatcher import EventDispatcher
from entity import Entity
from player import Player
from scenery import Scenery
from menu import Menu


class LanderApp:
    def __init__(self, w, h):
        
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, -150.0)
        self._space.damping = 0.8
        #self.space.sleep_time_threshold = 0.3

        # Physics
        # Frame rate
        self._fps = 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1
        # Time steps
        self._dt = 1.0/self._fps/self._physics_steps_per_frame       
        #self._dt = 1. / self._fps 

        # pygame
        pygame.init()
        
        if w==0 and h==0:
            self._screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
            self._w, self._h = pygame.display.Info().current_w, pygame.display.Info().current_h
        else:
            self._w, self._h = w,h
            self._screen = pygame.display.set_mode((self._w, self._h))
        
        
        self._clock = pygame.time.Clock()

        #self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        self._drawing = True

        # Static barrier walls (lines) that the balls bounce off of
        self.scenery = Scenery()
        self.scenery.add(self._space)
                
        # HUD
        self._font = pygame.font.SysFont("DejaVuSans", 24)
        self._text = self._font.render("Touch the screen.", True, (255, 255, 255, 255))
        self._text_w, self._text_h = self._text.get_size()
        self._add_hud()

        # Balls that exist in the world
        #self._balls = []
    
        # Player
        self.player = Player()
        self.player.add(self._space, Vec2d(self._w/2, self._h/2))

        # Add Event Dispatcher for user input
        self.ev = EventDispatcher()
                        
        # Menu
        self.menu = Menu()
               
        # Execution control 
        self._appRunning = True
        self._gameRunning = False
        self._isMenu = True
     
            
    def run(self):
        """
        The main loop of the game.
        :return: None
        """
        # Main loop             
        while self._appRunning:
           
            self._process_events()
            self._clear_screen()
                    
            if self._gameRunning:
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
        if self._isMenu:
            menu_choice = self.menu.update(self.menu, self)
            if menu_choice == "Play":
                self._isMenu = False
                self._gameRunning = True
			
			#if menu_choice == "Options":
			#	self.option_menu =
			
        if self._gameRunning:
            for event in self.ev.get():
                if event["type"] == self.ev.BTNDN:
                    self.player.input(event["idx"],1)
                elif event["type"]== self.ev.BTNUP:
                    self.player.input(event["idx"],0)
                elif event["type"] == self.ev.QUIT or event.type == self.ev.ESCAPE:
                    self._appRunning = False
                elif event["type"] == self.ev.DRAW:
                    self._drawing = not self._drawing
                
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
        if self._isMenu:
            self.menu.draw(self._screen)
            
        elif self._gameRunning:
            ### Draw space
            #self._space.debug_draw(self._draw_options)
            self.scenery.draw(self._screen)
            self.player.draw(self._screen)
    
        
    def _add_hud(self):
        pass
            
    def _update_hud(self):
        #fps_str = "fps: " + str(self._clock.get_fps())
        self._screen.blit(self._text, (self._w / 2 - self._text_w / 2, self._h / 2 - self._text_h / 2))


def main():
    app = LanderApp(0,0)
    app.run()

if __name__ == '__main__':
    main()







