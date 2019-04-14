# Allow pygame_sdl2 to be imported as pygame.
import pygame_sdl2
#pygame_sdl2.import_as_pygame()
import pygame

#import pymunk
#from pymunk import Vec2d

#import pymunk.pygame_util

#import sys

WITH_TOUCH = False

class EventDispatcher:

    NUM_BUTTONS = 3
        
    QUIT = 1
    ESCAPE = 2
    DRAW = 3
    DEBUGDRAW = 4
    VIDEORESIZE = 5
    VIDEOEXPOSE = 6
    ZOOMINC = 7
    ZOOMDEC = 8
    BTNDN = 10
    BTNUP = 20
     
    def __init__(self):
        self.btn_state = []
        for i in range(self.NUM_BUTTONS):
            self.btn_state.append(-1)    
                      
    def get(self):
        
        results = []
        
        for event in pygame.event.get():
            
            if WITH_TOUCH:
                if event.type == pygame.FINGERDOWN:
                    x, y  = event.x, event.y
                    f = event.fingerId
                    #w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
                    
                    i=2
                    if x < 1/3:
                        i = 0 #left
                    elif x > 1/3*2:
                        i = 1 # right
                    #else:
                    #    i = 2 # mid or both
                    
                    #sys.stderr.write("b {0:d}, x {1:f}, w{2:f}\n".format(i,x,w))
                    
                    if self.btn_state[i]==-1:
                        self.btn_state[i] = f
                        results.append({"type": self.BTNDN, "idx": i})

                #elif event.type == pygame.FINGERMOTION:
                    
                elif event.type == pygame.FINGERUP:
                    f = event.fingerId
                    for i in range (len(self.btn_state)):
                        if self.btn_state[i]==f:
                            self.btn_state[i]=-1
                            results.append({"type": self.BTNUP, "idx": i})
            else:

                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    results.append({"type": self.BTNDN, "idx": 0})
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    results.append({"type": self.BTNDN, "idx": 1})
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    results.append({"type": self.BTNDN, "idx": 2})
                elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                    results.append({"type": self.BTNUP, "idx": 0})
                elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                    results.append({"type": self.BTNUP, "idx": 1})
                elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
                    results.append({"type": self.BTNUP, "idx": 2})
                
                

            if event.type == pygame.QUIT:
                results.append({"type": self.QUIT})
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                results.append({"type": self.ESCAPE})
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                results.append({"type": self.DRAW})
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                results.append({"type": self.ZOOMINC})
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                results.append({"type": self.ZOOMDEC})            
            #elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            #    results.append({"type": self.DEBUGDRAWDRAW})
            elif event.type == pygame.VIDEORESIZE:
                results.append({"type": self.VIDEORESIZE, "w": event.w, "h": event.h})
            elif event.type == pygame.VIDEOEXPOSE:
                results.append({"type": self.VIDEOEXPOSE})
        
                
        return results    

