__author__ = 'Андрей'

import pygame
from Header import *


class Interface:
    def __init__(self,display,imgDict):
        self.imgDict=imgDict
        self.display=display
        self.FIELD_START_WIDTH=int(WINDOW_WIDTH/2-WINDOW_HEIGHT/5*2)
        self.FIELD_START_HEIGHT=int(WINDOW_HEIGHT/10)
        self.step=int(WINDOW_HEIGHT/10)

    def draw(self):
        self.display.fill((255,255,255))
        self.display.blit(self.imgDict["background.jpg"],(0,0))
        self.display.blit(self.imgDict["playing_field.png"],
                          (self.FIELD_START_WIDTH,
                           self.FIELD_START_HEIGHT))
        iRow=iColumn=0
        for row in self.field:
            for column in row:
                if column==1:
                    self.display.blit(self.imgDict["point_white.png"],
                                      (self.FIELD_START_WIDTH+iColumn*self.step,
                                       self.FIELD_START_HEIGHT+iRow*self.step))
                if column==-1:
                    self.display.blit(self.imgDict["point_black.png"],
                                      (self.FIELD_START_WIDTH+iColumn*self.step,
                                       self.FIELD_START_HEIGHT+iRow*self.step))
                iColumn+=1
            iColumn=0
            iRow+=1

    def restart(self):
        self.field = [[0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,-1,1,0,0,0],
                     [0,0,0,1,-1,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0]]