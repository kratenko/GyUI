'''
Created on 15.04.2012

@author: kra
'''

import resource

debug_theme = False

class ThemeProperty(object):

    def __init__(self, name):
        self.name = name
        self.cache_name = intern("_" + name)
    
    def __get__(self, obj, owner):
        if debug_theme:
            print "%s(%r).__get__(%r)" % (self.__class__.__name__, self.name, obj)
        try: ###
            cache_name = self.cache_name
            try:
                return getattr(obj, cache_name)
            except AttributeError, e:
                if debug_theme:
                    print e
                value = self.get_from_theme(obj.__class__, self.name)
                obj.__dict__[cache_name] = value
                return value
        except: ###
            if debug_theme:
                import traceback
                traceback.print_exc()
                print "-------------------------------------------------------"
            raise ###

    def __set__(self, obj, value):
        if debug_theme:
            print "Setting %r.%s = %r" % (obj, self.cache_name, value) ###
        obj.__dict__[self.cache_name] = value

    def get_from_theme(self, cls, name):
        return root.get(cls, name)


class FontProperty(ThemeProperty):

    def get_from_theme(self, cls, name):
        return root.get_font(cls, name)


class ThemeError(Exception):
    pass



class Theme(object):
    def __init__(self, name, base=None):
        self.name = name
        self.base = base
    
    def get(self, cls, name):
        try:
            return self.lookup(cls, name)
        except ThemeError:
            raise AttributeError("No value found in theme %s for '%s' of %s.%s" %
                (self.name, name, cls.__module__, cls.__name__))
    
    def lookup(self, cls, name):
        if debug_theme:
            print "Theme(%r).lookup(%r, %r)" % (self.name, cls, name)
        for base_class in cls.__mro__:
            class_theme = getattr(self, base_class.__name__, None)
            if class_theme:
                try:
                    return class_theme.lookup(cls, name)
                except ThemeError:
                    pass
        else:
            try:
                return getattr(self, name)
            except AttributeError:
                base_theme = self.base
                if base_theme:
                    return base_theme.lookup(cls, name)
                else:
                    raise ThemeError
    
    def get_font(self, cls, name):
        if debug_theme:
            print "Theme.get_font(%r, %r)" % (cls, name)
        spec = self.get(cls, name)
        if spec:
            if debug_theme:
                print "font spec =", spec
            return resource.get_font(*spec)


root = Theme('root')
root.font = (15, "Vera.ttf")
root.fg_color = (255, 255, 255)
root.bg_color = None
root.bg_image = None
root.scale_bg = False
root.border_width = 0
root.border_color = None
root.margin = 0
root.tab_bg_color = None
root.sel_color = (0, 128, 255)
root.highlight_color = None
root.disabled_color = None
root.highlight_bg_color = None
root.enabled_bg_color = None
root.disabled_bg_color = None

root.RootWidget = Theme('RootWidget')
root.RootWidget.bg_color = (0, 0, 0)

root.Button = Theme('Button')
root.Button.font = (18, "VeraBd.ttf")
root.Button.fg_color = (255, 255, 0)
root.Button.highlight_color = (255, 0, 0)
root.Button.disabled_color = (64, 64, 64)
root.Button.highlight_bg_color = None
root.Button.enabled_bg_color = None
root.Button.disabled_bg_color = None

#root.ImageButton = Theme('ImageButton')
#root.ImageButton.highlight_color = (0, 128, 255)

#root.CheckWidget = Theme('CheckWidget')
#root.CheckWidget.smooth = False

