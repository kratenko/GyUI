'''
Created on 14.04.2012

@author: kra
'''

import pygame

'''
Known signals to spot typos
'''
SIGNALS = set([
    'mouse_rest',
    'mouse_unrest',
    'mouse_over',
    'mouse_out',
    'button_down',
    'button_up',
    'click',
])



class GventException(Exception):
    '''
    Exceptions concerning Gvents
    '''
    pass



class Gvent(object):
    '''
    GyUI Event class
    
    everything that happens is passed to a subscriber via Gvents.
    '''
    def __init__(self, signal, pos=None, cascades=True):
        global SIGNALS
        if signal not in SIGNALS:
            raise GventException('Unknown signal for Gvent: %s' % signal)
        # created:
        self.created = pygame.time.get_ticks()
        
        # signal is the kind/name of the gvent
        self.signal = signal
        
        # still active? (=not stopped)
        self.active = True

        # receiver handling the event (for subscribers)
        self.receiver = None
        
        # receiver/widget the gvent is originated
        self.originator = None
        
        self.cascades = cascades

        # some cascade statistics
        self.receiver_touches = 0
        self.subscriber_touches = 0
        
        if pos:
            self.pos = pos
        
        
    def stop(self):
        self.active = False
        
        
    def is_active(self):
        return self.active
    
    def _detail_str(self):
        if self.signal == 'button_down':
            return "button:%d,repeat:%d,pos:%d,%d" % (self.button, self.repeat, self.pos[0], self.pos[1])
        return ''
    
    def __str__(self):
        return "<Gvent(%s.%d.%d,{%s})>" % (
                self.signal, 
                self.receiver_touches, 
                self.subscriber_touches,
                self._detail_str())



class GventReceiver(object):
    '''
    Base class for everything that handles gvents
    '''
    def __init__(self):
        self._subscribed = {}
        self.parent = None
        
        self.mouse_down_repeat = False
    
    
    def subscribe_gvent(self, signal, callable):
        '''
        Register a subscriber for a specific signal on this Receiver
        
        There can be multiple subscribers for one signal on the 
        same Receiver
        '''
        global SIGNALS
        if signal not in SIGNALS:
            raise GventException('Unknown signal for subscriber: %s' % signal)
        
        try:
            self._subscribed[signal].append(callable)
        except KeyError:
            self._subscribed[signal] = [callable]


    def send_gvent(self, gv):
        '''
        Send Gvent to this Receiver
        '''
        # is this the originator?
        if gv.originator is None:
            gv.originator = self
            
        # store in gvent, who is the receiver
        gv.receiver = self
        # first: look for subscribers in this receiver
        try:
            # first come, first go:
            for subscriber in self._subscribed[gv.signal]:
                subscriber(gv)
                # increase number of touches by subscribers
                gv.subscriber_touches += 1
                if not gv.is_active():
                    # gvent has been handled and stopped
                    return
        except KeyError:
            # do nothing, as this is same as unhandled gvent
            pass
        
        gv.receiver_touches += 1
        # pass to parent:
        if self.parent and gv.cascades:
            self.parent.send_gvent(gv)
        else:
            print "Gvent unhandled:", gv, "originator:", gv.originator
    
    
