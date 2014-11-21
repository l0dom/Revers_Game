__author__ = 'Андрей'

from pygame.locals import USEREVENT


END_SCENE =  USEREVENT + 1
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def mouseIn(mouse,start,end):
    if (mouse[0]>start[0])and(mouse[1]>start[1]):
        if (mouse[0]<end[0])and(mouse[1]<end[1]):
            return True
    return False


