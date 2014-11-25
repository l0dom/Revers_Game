__author__ = 'Андрей'

import pygame
from Header import *


class Interface:
    def __init__(self,display,imgDict,size):
        self.size=size
        self.imgDict=imgDict
        self.display=display
        self.FIELD_START_WIDTH=int(WINDOW_WIDTH/2-WINDOW_HEIGHT/5*2)
        self.FIELD_START_HEIGHT=int(WINDOW_HEIGHT/10)
        self.step=imgDict["block_black"].get_rect().h
        self.select = (WINDOW_WIDTH/2-self.step/2,WINDOW_HEIGHT-self.step)

    def draw(self,points,person,field,path={}):
        self.display.fill((255,255,255))
        self.display.blit(self.imgDict["background"],(0,0))

        blockName= "point_white" if person==1 else "point_black"
        self.display.blit(self.imgDict[blockName],self.select)

        iRow=iColumn=0
        for row in field:
            for column in row:
                blockName= "block_white" if (iColumn+iRow%2)%2==0 else "block_black"
                self.display.blit(self.imgDict[blockName],
                                  (self.FIELD_START_WIDTH+iColumn*self.step,
                                   self.FIELD_START_HEIGHT+iRow*self.step))
                if column==1:
                    self.display.blit(self.imgDict["point_white"],
                                      (self.FIELD_START_WIDTH+iColumn*self.step,
                                       self.FIELD_START_HEIGHT+iRow*self.step))
                if column==-1:
                    self.display.blit(self.imgDict["point_black"],
                                      (self.FIELD_START_WIDTH+iColumn*self.step,
                                       self.FIELD_START_HEIGHT+iRow*self.step))
                iColumn+=1
            iColumn=0
            iRow+=1

        for (keyX,keyY) in path:
            self.display.blit(self.imgDict["point"],
                              (self.FIELD_START_WIDTH+keyY*self.step,
                               self.FIELD_START_HEIGHT+keyX*self.step))

    def event(self):
        mouse = pygame.mouse.get_pos()
        mouse = mouse[0]-self.FIELD_START_WIDTH,mouse[1]-self.FIELD_START_HEIGHT
        if mouseIn(mouse,(0,0),(self.step*self.size,self.step*self.size)):
            return mouse[1]//self.step,mouse[0]//self.step
        else:
            return -1,-1