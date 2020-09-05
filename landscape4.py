from vpython import *

#we'll be making a grid of boxes
################################
Rows = 5
Cols = 5
showLabels =  Rows + Cols < 5
    
scene.center = vec(Rows, Cols, 0)
scene.height=800
scene.width=800

local_light(pos=vec(100,100,0), color=color.red)
local_light(pos=vec(-100,-100, 0), color=color.blue)

boxSize=0.9 #for "participation boxes" in cells 
boxDepth=0.1
amplifyHeight = sqrt(Rows)


#Utilities
##########
def avg(lst):
    return sum(lst)/len(lst)

def centroid(cell):
    x = avg( [v.pos.x for v in cell.vs] )
    y = avg( [v.pos.y for v in cell.vs] )
    z = avg( [v.pos.z for v in cell.vs] )
    return vec(x,y,z)

def colorFunc(height):
    """red in the valleys, blue in the peaks
        assumes height is -1 to 1
    """
    return vec( 0.1 - height,
                0.3 + height, 
                0.3 + height) 


#make vertices
vertices = dict()
def positionVertices():
    """Set showLabels = True for Labels"""
    for i in range(-1, 2*Rows+1):
        for j in range(-1, 2*Cols+1):
            pos = vec(i,j,0)
            l=label(pos=pos, text = f'v{i}{j}', visible = showLabels)  
            vertices[i,j] = vertex(pos=pos, initialPos = pos, label=l)
positionVertices()

# create a Unit class with a smart change method
# (use change to change size, height, BoxSize etc., not pos= as with vpython objects)
class Unit:
    def __init__(self, row,col,q):
        """
        A unit is a cell in a 2D matrix of rows and columns.
        All attributes should be changed using change()
        size denotes number of participants (agree, disagree, or pass)
        height and color denote agreement  (% agree)
            (height sets height AND color)
        boxSize denotes proportion of non-passes (no one passes, boxsize=1)
        """
        self.rowCol=(row,col)
        self.q = q
        boxPos = centroid(q)
        self.box =box(  pos = boxPos,
                        size= vec(boxSize,boxSize,boxDepth),
                        label=label(pos=boxPos + vec(0,-0.2,0), text=f'B{i}{j}',  color=color.green, visible= showLabels) )
     
        self.pos = self.box.pos
        self.size=1
        self.boxSize = boxSize
        self.height = 0
        self.color=color.magenta
        

    def change(self,color=None, pos=None, height=None, size=None, boxSize=None, rowCol = None, q=None):
        if rowCol is not None:
            self.rowCol = rowCol
            row,col=rowCol
            self.change(size=self.size)

        if q is not None:
            self.q = q
            self.change(color, self.color) #update the new vertices

        if color is not None:
            self.color=color
            self.box.color=color
            for i in range(4):
                self.q.vs[i].color=color
            
        if pos is not None:
            deltaVs = [0,0,0,0]
            self.pos = pos
            self.box.pos = pos
            self.change(size=self.size)

        if height is not None:
            newPos = vec(
                self.pos.x,
                self.pos.y,
                height)
            self.height=height
            newColor = colorFunc(height) * self.boxSize + vec(0.5,0.5,0.5)
            self.change(pos=newPos, color =newColor )
        
        if boxSize is not None: #boxsize is relative to cell size; 1 means no visible frame
            self.boxSize=boxSize
            self.box.size = self.boxSize * vec(self.size,self.size,0.2)
            
        if size is not None: # voters
            self.size=size
            TR, TL, BL, BR = 0,1,2,3 #T is top, B is Bottom
            target=self.q
            wide=long=size
            target.vs[TR].pos.x = target.vs[TL].pos.x + wide
            target.vs[BR].pos.x = target.vs[BL].pos.x + wide
            target.vs[TR].pos.y = target.vs[BR].pos.y + long
            target.vs[TL].pos.y = target.vs[BL].pos.y + long
            for i in range(4):
                target.vs[i].pos.z = self.height

            self.boxSize = size
            self.box.size = self.boxSize * vec(size,size,boxDepth)

            newPos= target.vs[BL].pos + vec(size/2, size/2,0)
            self.pos = newPos
            self.box.pos = newPos
    

# make quads, cells, boxes and use them to build units.  
quads   =  dict()
boxes =    dict()
units =    dict()
for i in range(2*Rows+1):
    for j in range( 2*Cols+1):
        vs=[    vertices[i,j],
                vertices[i-1,j],
                vertices[i-1,j-1],
                vertices[i, j-1]    ]

        q = quad(vs=vs,
            texture=textures.rough,
            shininess=0,)
        q.label = label(pos=centroid(q), text=f'Q{i}{j}', color=color.yellow, visible=showLabels)

        quads[i,j] = q

        if i%2 and j%2:
            row, col = i//2, j//2
            #print(row,col)
            q = quads[i,j]
            q.visible=False
            u = Unit(row,col,q) #CREATE the unit
            units[row,col] = u

from random import random
def initLandscape(): #random landscape
    for row in range(Rows):
        for col in range(Cols):
            height= 1 - (2*random()) # -1 to 1
            color=colorFunc(height) 
            size=random()
            boxSize=random()
            units[row,col].change(  height=height * amplifyHeight, #visual height can be amplified
                                    color=color, 
                                    size=size, 
                                    boxSize=boxSize) #use the changemethod

initLandscape()

###### sorting 
def sliceDict(XorY='X', index=0,  boxMat = units):
    """ return a dictionary containing the cells of a single column or Row
    ('X', 0) is the first column (all cells with X=0)  
    """

    if XorY=='X':
        ret = [[k,v] for k,v in boxMat.items() if k[0]== index]   
    else:
        if XorY!='Y':
            raise Exception('ERROR: rowOrCol must be "X" or "Y"')
            return
        ret = [[k,v] for k,v in boxMat.items() if k[1]== index]   

    #turn the list of tuples into a dictionary
    retDict=dict()
    for k,v in ret:
        retDict[k] = v

    return retDict

#####Sort the full grid.

for XorY in ['X','Y']:
    for index in range(Cols):
        sleep(0.1)
        SD = sliceDict(XorY, index, units)
        Have = list(SD.values())

        metric = [u.height for u in SD.values()]
        shuffled = sorted(list(zip(metric,SD.items())))
        Wants = []
        for i,(m,(k,u)) in enumerate(shuffled):
            Wants.append(u)
            
        #store the props of the wants
        #then apply them to the Haves

        #store...
        wantedProps = []
        for want in Wants:
            wantedProps.append(dict(
                size   = want.size,
                height = want.height,
                boxSize= want.boxSize
            ))

        #apply
        for i, want in enumerate(wantedProps):
            Have[i].change(
                size=want['size'],
                height=want['height'],
                boxSize=want['boxSize'])
