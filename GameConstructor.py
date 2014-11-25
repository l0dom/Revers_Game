__author__ = 'Андрей'

from random import randint
from pygame import MOUSEBUTTONUP

''' 0-empty
    1-white
    2-black'''

'''players'''
def playerMan(self,event):
        pair = -1,-1
        for e in event.get():
            if e.type == MOUSEBUTTONUP:
                pair =  self.interface.event()
        return pair

def playerPC(self,event):
    maxValue = -1
    pairs = []
    for key in self.validPath:
        if len(self.validPath[key]) == maxValue:
            pairs.append(key)
        if len(self.validPath[key]) > maxValue:
            pairs=[key]
            maxValue = len(self.validPath[key])
    rnd=randint(0,len(pairs)-1)
    return pairs[rnd]
'''end players'''

'''revers'''
def reversDescend (self,x,y):
    if (x,y) in self.validPath:
        person=self.person
        self.field[x][y]=person
        for value in self.validPath[(x,y)]:
            self.field[value[0]][value[1]]=person
        self.points[person]+=1
        self.person = 1 if self.person==-1 else -1
        self.validPath = self._getValidPath()

def reversStart (self,size):
    self.field = []
    self.size=size
    for i in range(size):
        self.field.append([0] * size)
    middle=int(size/2-1)
    self.field[middle][middle]=-1
    self.field[middle+1][middle]=1
    self.field[middle][middle+1]=1
    self.field[middle+1][middle+1]=-1

def __reversGVPSearch(field,X,Y,person):
    directions = [(-1,1),(-1,0),(-1,-1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    size = len(field)
    deletePath= []
    for direction in directions:
        tmpPath = []
        x=X+direction[0]
        y=Y+direction[1]
        while (0<=x<size)and(0<=y<size)and(field[x][y]==-person):
            tmpPath.append((x,y))
            x+=direction[0]
            y+=direction[1]
        if (0<=x<size)and(0<=y<size)and(field[x][y]==person):
            deletePath+=tmpPath
    return deletePath

def reversGVP(self):
    validPath={}
    person = self.person
    for row in range(0,self.size):
        for column in range(0,self.size):
            if self.field[row][column]==0:
                part = __reversGVPSearch(self.field, row, column, person)
                if len(part) != 0:
                    validPath[(row,column)] = part
    return validPath

def reversEvent(self):
    if len(self.validPath)==0:
        self.person = 1 if self.person==-1 else -1
        self.validPath=self._getValidPath()
        if len(self.validPath)==0:
            self.end=True
'''end_revers'''


class GameConstructor:
    def __init__(self,interface,size,getValidPath,descend,start,event,playerOne,playerTwo):
        self.interface=interface
        self.getValidPath=getValidPath
        self.descend=descend
        self.start=start
        self.event=event
        rnd=randint(0,1)
        self.players= {1-2*rnd: playerOne, -1+2*rnd: playerTwo}

        self.person = 1
        self.end=False
        self._start(size)
        self.validPath = self._getValidPath()
        self.points = {-1:0,1:0}
        self.active =False
        self.load = 0


    def _descend(self,x,y):
        if self.active:
            self.descend(self,x,y)
            self.active=False
            self.load=0

    def _getValidPath(self):
        return self.getValidPath(self)

    def _start(self,size):
        self.start(self,size)

    def _event(self,events):
        self.event(self)
        pair = self.players[self.person](self,events)
        if pair[0]!=-1:
            self._descend(pair[0],pair[1])

    def update (self,dt):
        if self.active==False:
            if self.load<=500:
                self.load+=dt
            else:
                self.active=True

    def draw(self):
        self.interface.draw(self.points,
                    self.person,
                    self.field,
                    self.validPath)

