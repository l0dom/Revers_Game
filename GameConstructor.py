__author__ = 'Андрей'

from random import randint
from pygame import MOUSEBUTTONUP
from online import *

''' 0-empty
    1-white
    2-black'''

'''players'''
def playerMan(self,event):
    pair = -1,-1
    for e in event.get():
        if e.type == MOUSEBUTTONUP:
            pair =  self.interface.event()
    if self.online:
        self.server.sendPickle(pair)
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
    if len(pairs)!=0:
        rnd=randint(0,len(pairs)-1)
        return pairs[rnd]
    else:
        return -1,-1

def playerOnline(self,event):
    return self.server.getPickle()

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

    self.getValidPath=reversGVP
    self.descend=reversDescend
    self.event=reversEvent
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
            if self.players[-1]==playerMan or self.players[1]==playerMan:
                if self.points[-1]==self.points[1]:
                    self.message = "Tie!"
                elif self.points[-1]>self.points[1]:
                    self.message = "Black win!"
                else:
                    self.message = "White win!"
            else:
                self.message = "bots played"
'''end_revers'''


'''revers black hall'''
def reversBlackHallStart (self,size):
    reversStart(self,size)
    success = False
    while not success:
        x=randint(0,size-1)
        y=randint(0,size-1)
        if self.field[x][y] == 0:
            self.field[x][y] = 2
            success=True
'''end revers black hall'''

'''online'''
def startHost(self,size):
    self.server = Host()
    self.server.start()
    self.server.sendPickle((self.gameType,self.rnd,size))
    startFunc[self.gameType](self,size)

def startClient(self,size):
    self.server = Client()
    self.server.start("127.0.0.1")
    self.gameType,self.rnd,size=self.server.getPickle()
    self.rnd = 1 - self.rnd
    startFunc[self.gameType](self,size)
'''end online'''

startFunc={"revers":reversStart,
           "reversBH":reversBlackHallStart}

class GameConstructor:
    def __init__(self,interface,gameType,playerOne,playerTwo,onlineStart=None,size=8):
        self.gameType=gameType
        if onlineStart is None:
            self.start=startFunc[gameType]
            self.online = False
        else:
            self.start=onlineStart
            self.online = True
        self.interface=interface
        self.person = 1
        self.end=False
        self.rnd=randint(0,1)
        self._start(size)
        self.players= {1-2*self.rnd: playerOne, -1+2*self.rnd: playerTwo}
        self.validPath = self._getValidPath()
        self.points = {-1:2,1:2}
        self.active =False
        self.load = 0
        self.message = None



    def _descend(self,x,y):
        if self.active:
            self.descend(self,x,y)
            self.active=False
            self.load=0
            self.interface.animated=True
            self.points = self.points = {-1:0,1:0}
            for row in self.field:
                for column in row:
                    if column==1 or column ==-1:
                        self.points[column]+=1

    def _getValidPath(self):
        return self.getValidPath(self)

    def _start(self,size):
        self.start(self,size)

    def _event(self,events):
        self.event(self)
        pair = self.players[self.person](self,events)
        if pair[0]!=-1:
            self._descend(pair[0],pair[1])
        if self.online:
            if self.server.error is not None:
                self.end=True
                self.message = 'Connection lost'

    def update (self,dt):
        if self.active==False:
            if self.load<=1000:
                self.load+=dt
            else:
                self.active=True

    def draw(self):
        path = self.validPath if self.players[self.person]==playerMan else {}
        self.interface.draw(self.points,
                    self.person,
                    self.field,
                    path)


