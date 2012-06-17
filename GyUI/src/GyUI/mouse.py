'''
Created on 14.04.2012

@author: kra
'''

import pygame
import gvent

REST_TIME = 750
CLICK_REPEAT_TIME = 500

DOWN_REPEAT_START = 300
DOWN_REPEAT_REPEAT = 150

MOUSE_LEFT_BUTTON = 1
MOUSE_RIGHT_BUTTON = 3
MOUSE_WHEEL_BUTTON = 2
MOUSE_WHEEL_UP = 4
MOUSE_WHEEL_DOWN = 5
MOUSE_BUTTON_INDEX_MAX = 7


class Mouse(object):
    def _button_xrange(self): 
        global MOUSE_BUTTON_INDEX_MAX
        return xrange(MOUSE_BUTTON_INDEX_MAX+1)
    
    
    def _button_range(self):
        global MOUSE_BUTTON_INDEX_MAX
        return range(MOUSE_BUTTON_INDEX_MAX+1)
    
    
    def _button_list(self, value=None):
        '''
        Return a list for mouse buttons initialised with value.
        '''
        return [value for _ in self._button_xrange()]
    
    
    def __init__(self, shell):
        self.shell = shell
        # current position of mouse cursor
        self.pos = (0,0)
        # mouse cursor position in last update
        self.old_pos = (0,0)
        # ticks of last update
        self.last_update = 0
        # ticks since last mouse movement
        self.resting_time = 0
        # mouse currently resting?
        self.resting = False

        self.over = None
        self.over_stack = []
        
        self.down_time = self._button_list(0)
        self.down_pos = self._button_list((0,0))
        
        self.down_gvent = self._button_list(None)
        self.down_repeat = self._button_list(None)
        self.down_repeat_count = self._button_list(0)
        self.click_count = self._button_list(0)
        self.click_time = self._button_list(0)


        
    
    def update_position(self):
        '''
        Update mouse position
        '''
        global REST_TIME
        now = pygame.time.get_ticks()
        
        self.old_pos = self.pos
        self.pos = pygame.mouse.get_pos()
        # get topmost widget, mouse is over
        over_now = self.shell.get_widget_at(self.pos)
        
        if self.pos == self.old_pos:
            # mouse didn't move
            self.resting_time += now-self.last_update
            if (not self.resting) and self.resting_time>=REST_TIME:
                self.resting = True
                gv = gvent.Gvent('mouse_rest', pos=self.pos)
                over_now.send_gvent(gv)
#                print "Rest On"
        else:
            # mouse did move
            self.resting_time = 0
            if self.resting:
                self.resting = False
                gv = gvent.Gvent('mouse_unrest', pos=self.pos)
                # TODO: maybe store widget from rest and use here?
                over_now.send_gvent(gv)
                
        # handle mouse down repeats:
        global DOWN_REPEAT_REPEAT
        for button in self._button_xrange():
            if self.down_repeat[button] and self.down_repeat[button] <= now:
                # repeat mouse down gvent:
                self.down_repeat[button] = now + DOWN_REPEAT_REPEAT
                self.down_repeat_count[button] += 1
                gv_d = self.down_gvent[button]
                gv_r = gvent.Gvent('button_down', pos=gv_d.pos)
                gv_r.button = gv_d.button
                gv_r.repeat = self.down_repeat_count[button]
                # mess a bit with originator and receiver to
                # skip cascading:
                gv_r.originator = gv_d.originator
                gv_d.receiver.send_gvent(gv_r)
                
        
        # handle mouse over and mouse out
        if over_now is not self.over:
            # topmost under mouse changed:
            old_stack = []
            new_stack = []
            p = self.over
            while p is not None:
                old_stack.append(p)
                p = p.parent
            p = over_now
            while p is not None:
                new_stack.append(p)
                p = p.parent
            # remove identic tails:
#            print "old:", old_stack
#            print "new:", new_stack
            try:
                while old_stack[-1] == new_stack[-1]:
                    old_stack.pop()
                    new_stack.pop()
            except IndexError:
                # one list is empty, thats fine...
                pass
            # mouse outs
            for w in old_stack:
                gv = gvent.Gvent("mouse_out", pos=self.pos, cascades=False)
                w.send_gvent(gv)
            # mouse overs (other way around)
            for w in new_stack[::-1]:
                gv = gvent.Gvent("mouse_over", pos=self.pos, cascades=False)
                w.send_gvent(gv)
            self.over = over_now
                
        # store time of last update
        self.last_update = now
        
    
    def evaluate_button_down(self, ev):
        recv = self.shell.get_widget_at(ev.pos)
        
        button = ev.button
        
        gv = gvent.Gvent('button_down', pos=ev.pos)
        gv.button = button
        gv.repeat = 0
        # store gvent for later use
        self.down_gvent[button] = gv
        
#        self.down_widget[button] = 
        recv.send_gvent(gv)
        
        if gv.receiver:
            # was down received by a down repeater widget?
            if gv.receiver.mouse_down_repeat:
                global DOWN_REPEAT_START
                self.down_repeat[button] = gv.created + DOWN_REPEAT_START
                self.down_repeat_count[button] = 0 
                
        
#        recv.handle_gvent(gv)
        #print "down at", w
        
    
    def evaluate_button_up(self, ev):
        recv = self.shell.get_widget_at(ev.pos)
        
        button = ev.button
    
        # button up gvent:    
        gv_up = gvent.Gvent('button_up', pos=ev.pos)
        gv_up.button = button
        recv.send_gvent(gv_up)
        
        # click event:
        gv_down = self.down_gvent[button]
        down_widget = gv_down.originator
        if down_widget:
            gv_click = gvent.Gvent('click', pos=ev.pos)
            gv_click.button = button
            gv_click.duration = gv_click.created - gv_down.created
            
            global CLICK_REPEAT_TIME
            if gv_click.created - self.click_time[button] <= CLICK_REPEAT_TIME:
                self.click_count[button] += 1
            else:
                self.click_count[button] = 1
            gv_click.click = self.click_count[button]
            self.click_time[button] = gv_down.created

            down_widget.send_gvent(gv_click)
        
        # clean up down_repeat
        self.down_repeat[button] = 0
#        self.down_repeat_count[button] = 0
    