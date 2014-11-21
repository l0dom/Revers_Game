__author__ = 'Андрей'


''' 0-empty
    1-white
    -1-black'''

'''revers'''
def reversDescend (self,x,y):
    person=self.person
    self.field[y][x]=person
    for value in self.validPath[(x,y)]:
        self.field[value[1]][value[0]]=person
    self.person = 1 if self.person==-1 else -1
    self.validPath = self._getValidPath()
    if len(self.validPath)==0:
        self.person = 1 if self.person==-1 else -1
    self.steps+=1

def reversStart (self,size):
    self.field = []
    self.size=size
    for i in range(size):
        self.field.append([0] * size)
    self.steps = 4
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
        while (0<x<size)and(0<y<size)and(field[x][y]==-person):
            tmpPath.append((x,y))
            x+=direction[0]
            y+=direction[1]
        if (0<x<size)and(0<y<size)and(field[x][y]==person):
            deletePath+=tmpPath
    return deletePath

def reversGVP(self):
    validPath={}
    person = self.person
    for x in range(0,self.size):
        for y in range(0,self.size):
            if self.field[y][x]==0:
                part = __reversGVPSearch(self.field, x, y, person)
                if len(part) != 0:
                    validPath[(x,y)] = part
    return validPath
'''end_revers'''


class GameConstructor:
    def __init__(self,size,getValidPath,descend,start):
        self.getValidPath=getValidPath
        self.descend=descend
        self.start=start
        self.person = 1
        self._start(size)
        self.validPath = self._getValidPath()


    def _descend(self,x,y):
        self.descend(self,x,y)

    def _getValidPath(self):
        return self.getValidPath(self)

    def _start(self,size):
        self.start(self,size)


