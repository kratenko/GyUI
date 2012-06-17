'''
Created on 15.04.2012

@author: kra
'''

import os, sys, logging

import pygame

logger = logging.getLogger("GyUI.resource")

# constants
RESOURCE_DIR_NAME = 'res'


# caches:
font_cache = {}



class ResourceException(Exception):
    pass



def find_resource_dir():
    global RESOURCE_DIR_NAME
    # start path, script location:
    dir = sys.path[0]
    while True:
        path = os.path.join(dir, RESOURCE_DIR_NAME)
        if os.path.exists(path):
            return path
        parent = os.path.dirname(dir)
        if parent == dir:
            raise ResourceException("could not find resource directory")
        dir = parent


resource_dir = find_resource_dir()        
#logger.info('found resource directory at "%s"' % resource_dir)
print ('found resource directory at "%s"' % resource_dir)


def _resource_path(default_prefix, names, prefix = ""):
    return os.path.join(resource_dir, prefix or default_prefix, *names)


def get_font(size, *names):
    font_path = _resource_path('font', names)
    key = (font_path, size)
    font = font_cache.get(key)
    if not font:
        font = pygame.font.Font(font_path, size)
        font_cache[key] = font
    return font
    


