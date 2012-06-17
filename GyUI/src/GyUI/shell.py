'''
Created on 14.04.2012

@author: kra
'''

import pygame
import mouse, gvent

shell = None

def get_shell():
    global shell
    if shell is None:
        pygame.init()
        display = pygame.display.set_mode((320,240), 0)
        shell = Shell(display)
    return shell



class Shell(object):
    def __init__(self, display):
        self.mouse = mouse.Mouse(self)
        self.display = display
        self.running = True
        self.clock = pygame.time.Clock()
        self.frame_rate = 30
        
        self.mask = None
        
        
    def run(self):
        # we don't need mouse move events
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        while self.running:
            self.mouse.update_position()
            events = pygame.event.get()
            for ev in events:
                type = ev.type
                if type == pygame.QUIT:
                    self.running = False
                    # quit event handling loop
                    break
                elif type == pygame.MOUSEBUTTONDOWN:
                    self.mouse.evaluate_button_down(ev)
                elif type == pygame.MOUSEBUTTONUP:
                    self.mouse.evaluate_button_up(ev)
#                elif type == pygame.ACTIVEEVENT and ev.state==1:
#                    # Mouse active event (mouse leaving of :
#                    self.mouse.handle_active(ev)
#                    print "MOUS"
#                    pass
                else:
                    print "slipped event:", ev
                    
            # draw all updates:
            to_update = self.draw()
            # update screen
            pygame.display.update(to_update)
            
            # wait rest of frame
            self.clock.tick(self.frame_rate)
    
    
    def draw(self):
        return self.mask.draw(self.display)
        
    
    def get_widget_at(self, pos):
        return self.mask.get_widget_at(pos)
