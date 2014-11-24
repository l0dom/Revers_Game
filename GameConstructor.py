__author__ = 'Андрей'


''' 0-empty
    1-white
    -1-black'''

'''revers'''
def reversDescend (self,x,y):
    if (x,y) in self.validPath:
        person=self.person
        self.field[x][y]=person
        for value in self.validPath[(x,y)]:
            self.field[value[0]][value[1]]=person
        self.steps[person]+=1
        self.person = 1 if self.person==-1 else -1
        self.validPath = self._getValidPath()

def reversStart (self,size):
    self.field = []
    self.size=size
    for i in range(size):
        self.field.append([0] * size)
    self.steps = {-1:0,1:0}
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
    def __init__(self,size,getValidPath,descend,start,event):
        self.getValidPath=getValidPath
        self.descend=descend
        self.start=start
        self.event=event
        self.person = 1
        self.end=False
        self._start(size)
        self.validPath = self._getValidPath()


    def _descend(self,x,y):
        self.descend(self,x,y)

    def _getValidPath(self):
        return self.getValidPath(self)

    def _start(self,size):
        self.start(self,size)

    def _event(self):
        self.event(self)

