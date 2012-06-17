'''
Created on 15.04.2012

@author: kra
'''

import pygame
from widget import Widget, overridable_property
from theme import ThemeProperty


class Label(Widget):
    text = overridable_property('text')
    align = overridable_property('align')

    highlight_color = ThemeProperty('highlight_color')
    disabled_color = ThemeProperty('disabled_color')
    highlight_bg_color = ThemeProperty('highlight_bg_color')
    enabled_bg_color = ThemeProperty('enabled_bg_color')
    disabled_bg_color = ThemeProperty('disabled_bg_color')
    
    enabled = True
    highlighted = False
    _align = 'l'
    
    def __init__(self, text, width = None, **kwds):
        Widget.__init__(self, **kwds)
        font = self.font
        self.set_text(text)
        return
    
        lines = text.split("\n")
        tw, th = 0, 0
        for line in lines:
            w, h = font.size(line)
            tw = max(tw, w)
            th += h
        if width is not None:
            tw = width
        else:
            tw = max(1, tw)
        d = 2 * self.margin
        self.size = (tw + d, th + d)
        self._text = text
    
    
    def get_text(self):
        return self._text
    
    def _render_image(self):
        '''
        Render image to be blited on draw
        '''
        line_height = self.font.get_linesize()
        lines = self._text.split("\n")
        fg = self.fg_color
        bg = self.bg_color
        line_images = []
        line_width = 0
        for line in lines:
            print bg
            img = self.font.render(line, True, fg)
            line_width = max(line_width, img.get_width())
            line_images.append(img)
        space = self.border_width + self.margin
        self.width = 2*space + line_width
        self.height = 2*space + len(line_images)*line_height
        self._image = pygame.Surface(self.size)
        if bg:
            self._image.fill()
        dest = pygame.Rect((0,0),(self.width,line_height))
        for img in line_images:
            dest.width = img.get_width()
            if self.align=='c':
                dest.centerx = self.width/2
            elif self.align=='r':
                dest.right = self.width
#            else:
#                dest.left = 0
            # blit it
            self._image.blit(img, dest)
            dest.top += dest.height
            
            
    
    def set_text(self, text):
        self._text = text
        self._render_image()
    
    
    def get_align(self):
        return self._align
    
    def set_align(self, x):
        self._align = x
        self._render_image()

    def draw(self, surface):
        surface.blit(self._image, self.rect)


    def draw_with(self, surface, fg, bg = None):
        if bg:
            r = surface.get_rect()
            b = self.border_width
            if b:
                e = - 2 * b
                r.inflate_ip(e, e)
            surface.fill(bg, r)
        m = self.margin
        align = self.align
        width = surface.get_width()
        y = m
        lines = self.text.split("\n")
        font = self.font
        dy = font.get_linesize()
        for line in lines:
            image = font.render(line, True, fg)
            r = image.get_rect()
            r.top = y
            if align == 'l':
                r.left = m
            elif align == 'r':
                r.right = width - m
            else:
                r.centerx = width // 2
            surface.blit(image, r)
            y += dy



#class Button(widget.Label):
#    pass

