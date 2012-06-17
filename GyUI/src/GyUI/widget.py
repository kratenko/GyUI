'''
Created on 14.04.2012

@author: kra
'''

import logging

import pygame

import gvent
from theme import ThemeProperty, FontProperty


def overridable_property(name, doc = None):
    """Creates a property which calls methods get_xxx and set_xxx of
    the underlying object to get and set the property value, so that
    the property's behaviour may be easily overridden by subclasses."""
    
    getter_name = intern('get_' + name)
    setter_name = intern('set_' + name)
    return property(
        lambda self: getattr(self, getter_name)(),
        lambda self, value: getattr(self, setter_name)(value),
        None,
        doc)


def rect_property(name):
    def get(self):
        return getattr(self._rect, name)
    def set(self, value):
#        print 'global', self, value
        r = self._rect
        old_size = r.size
        setattr(r, name, value)
        new_size = r.size
        self._rect_global_to_local()
        if old_size <> new_size:
            self._resized(old_size)
    return property(get, set)


def local_rect_property(name):
    def get(self):
        return getattr(self._local_rect, name)
    def set(self, value):
#        print 'local', self, value
        r = self._local_rect
        old_size = r.size
        setattr(r, name, value)
        new_size = r.size
        self._rect_local_to_global()
        if old_size <> new_size:
            self._resized(old_size)
    return property(get, set)


class Widget(gvent.GventReceiver):
    logger = logging.getLogger("GyUI.Widget")

    font = FontProperty('font')
    fg_color = ThemeProperty('fg_color')
    bg_color = ThemeProperty('bg_color')
    bg_image = ThemeProperty('bg_image')
    scale_bg = ThemeProperty('scale_bg')
    border_width = ThemeProperty('border_width')
    border_color = ThemeProperty('border_color')
    sel_color = ThemeProperty('sel_color')
    margin = ThemeProperty('margin')
    menu_bar = overridable_property('menu_bar')
    is_gl_container = overridable_property('is_gl_container')

    
    # rect properties accesses
    left = rect_property('left')
    right = rect_property('right')
    top = rect_property('top')
    bottom = rect_property('bottom')
    width = rect_property('width')
    height = rect_property('height')
    size = rect_property('size')
    topleft = rect_property('topleft')
    topright = rect_property('topright')
    bottomleft = rect_property('bottomleft')
    bottomright = rect_property('bottomright')
    midleft = rect_property('midleft')
    midright = rect_property('midright')
    midtop = rect_property('midtop')
    midbottom = rect_property('midbottom')
    center = rect_property('center')
    centerx = rect_property('centerx')
    centery = rect_property('centery')
    
    # local_rect properties accesses
    local_left = local_rect_property('left')
    local_right = local_rect_property('right')
    local_top = local_rect_property('top')
    local_bottom = local_rect_property('bottom')
    local_width = local_rect_property('width')
    local_height = local_rect_property('height')
    local_size = local_rect_property('size')
    local_topleft = local_rect_property('topleft')
    local_topright = local_rect_property('topright')
    local_bottomleft = local_rect_property('bottomleft')
    local_bottomright = local_rect_property('bottomright')
    local_midleft = local_rect_property('midleft')
    local_midright = local_rect_property('midright')
    local_midtop = local_rect_property('midtop')
    local_midbottom = local_rect_property('midbottom')
    local_center = local_rect_property('center')
    local_centerx = local_rect_property('centerx')
    local_centery = local_rect_property('centery')
    
    
    def __init__(self, rect=None):
        '''
        Constructor for Widget
        '''
        gvent.GventReceiver.__init__(self)
        
        self.dirty = 1
        self.parent = None
        if rect is None:
            self._rect = pygame.Rect((0, 0), (100, 100))
        elif rect:
            self._rect = pygame.Rect(rect)
#            self._rect = rect
        self._local_rect = pygame.Rect((0, 0), (100, 100)) 
    
    
    def get_rect(self):
        '''
        Getter for rect property
        '''
        return self._rect
    
    
    def set_rect(self, rect):
        '''
        Setter for rect property
        '''
        old_rect = self._rect
        self._rect = pygame.Rect(rect)
        self._rect_global_to_local()
        self._moved(old_rect.topleft)
        self._resized(old_rect.size)
    
    rect = property(get_rect, set_rect)
    
    
    def get_local_rect(self):
        '''
        Getter for local_rect property
        '''
        return self._local_rect
    
    
    def set_local_rect(self, rect):
        '''
        Setter for local_rect property
        '''
        old_rect = self._local_rect
        self._local_rect = pygame.Rect(rect)
        self._rect_local_to_global()
        self._moved(old_rect.topleft)
        self._resized(old_rect.size)

    local_rect = property(get_local_rect, set_local_rect)
    
    
    def _rect_global_to_local(self):
        '''
        Set local rect from global rect
        '''
        if self.parent:
            move_by = (self.parent.left*-1, self.parent.top*-1)
            self._local_rect = self._rect.move(move_by)
        else:
            self._local_rect = self._rect
        print self, "new local_rect:", self._local_rect
            
            
    def _rect_local_to_global(self):
        '''
        Set global rect from local rect
        '''
        if self.parent:
            self._rect = self._local_rect.move(self.parent.topleft)
        else:
            self._rect = self._local_rect
            

    def _resized(self, old_size):
        '''
        Inform widget that it's size has changed
        '''
        if self._rect.size != tuple(old_size):
            # new size is different
            pass
    
    
    def _moved(self, old_pos):
        if self._rect.topleft != tuple(old_pos):
            # new pos is actually different
            self.set_dirty()
    
    
    def _parent_moved(self, old_pos):
        # recalculate local rect with new parent position
        self._rect_local_to_global()
            
    
    def _set_parent(self, parent):
        self.parent = parent
#        self._parent_resized(None)
        self._parent_moved(None)
    
    
    
    
    def get_widget_at(self, pos):
        '''
        Get widged at that (global) position
        
        This is mainly useful as recursion end from Bin widgets 
        '''
        return self
    
    
    
    
    def _draw(self, surface):
        '''
        Execute actual draw of this very widget
        '''
        pygame.draw.rect(surface, (0xff,0,0), self.rect)
    
    
    def draw(self, surface):
        '''
        '''
        self._draw(surface)
    
    
    def set_dirty(self):
        '''
        Set this widget to be redrawn next draw
        '''
        if not self.dirty:
            self.dirty = 1
            
            
    def set_dirty_all(self):
        self.set_dirty()
            


class Bin(Widget):
    def __init__(self, rect=None):
        Widget.__init__(self, rect)
        self.children = []
    
    
    def draw(self, surface):
        self._draw(surface)
        for child in self.children:
            child.draw(surface)

    
    def get_widget_at(self, pos):
        for widget in self.children[::-1]:
#            if widget.visible:
#                r = widget.rect
                if widget.rect.collidepoint(pos):
                    return widget.get_widget_at(pos)
#                    return widget.find_widget(numpy.subtract(pos, r.topleft))
        return self
        
    
    def _moved(self, old_pos):
        if self._rect.topleft != tuple(old_pos):
            # new pos is actually different
            # inform children of movement
            for child in self.children:
                child._parent_moved(old_pos)
    
    
    def _parent_moved(self, old_pos):
        # recalculate local rect with new parent position
        self._rect_local_to_global()
        for child in self.children:
            child._parent_moved(old_pos)


    def add_widget(self, wid, pos=None):
        '''
        Add new child widget to widget
        '''
        self.children.append(wid)
        wid._set_parent(self)
        if pos:
            wid.local_topleft = pos


    def set_dirty_all(self):
        '''
        Set this widget and it's children to be redrawn next draw
        '''
        self.set_dirty()
        for child in self.children:
            child.set_dirty_all()



class Block(Widget):
    def __init__(self, (w, h), color):
        Widget.__init__(self)
        self.local_rect = (0, 0, w, h)
        self.color = color
        
        
    def _draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)



class Label(Widget):
    font = None
    def __init__(self, text):
        Widget.__init__(self)
        if self.font is None:
            self.font = pygame.font.Font("../../res/font/Vera.ttf", 10)
        self.set_text(text)
#        self.text = text


    def set_text(self, text):
        self.text = text
        self.rendered = self.font.render(self.text, True, (0x80, 0x80, 0x00), (0,0,0))
        self.size = self.rendered.get_size()
        self.set_dirty()


    def _draw(self, surface):
        surface.blit(self.rendered, self.rect)
        return [self.rect]
    
