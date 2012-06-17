'''
Created on 14.04.2012

@author: kra
'''

import pygame
import widget

class Mask(widget.Bin):
    def __init__(self):
        widget.Bin.__init__(self, ((0, 0), pygame.display.get_surface().get_size()))
        pass

    def start(self):
        pass
    
    def stop(self):
        pass
    
    def _draw(self, surface):
        pass
    
    def draw(self, surface):
        # call superclass
        widget.Bin.draw(self, surface)
        return [self.rect]
        
    