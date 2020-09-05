from vpython import *

#we'll be making a grid of boxes
Rows = 5
Cols = 5
showLabels =  Rows + Cols < 5
    
scene.center = vec(Rows, Cols, 0)
scene.height=800
scene.width=800
#scene.axis = vec(0.17653, 0.857299, -0.483607)

local_light(pos=vec(100,100,0), color=color.red)
local_light(pos=vec(-100,-100, 0), color=color.blue)

boxSize=0.9 #for "participation boxes" in cells 
boxDepth=0.1

#make vertices
vertices = dict()
def positionVertices():
    for i in range(-1, 2*Rows+1):
        for j in range(-1, 2*Cols+1):
            pos = vec(i,j,0)
            l=label(pos=pos, text = f'v{i}{j}', visible = showLabels)  
            vertices[i,j] = vertex(pos=pos, initialPos = pos, label=l)
positionVertices()

def avg(lst):
    return sum(lst)/len(lst)

def centroid(cell):
    x = avg( [v.pos.x for v in cell.vs] )
    y = avg( [v.pos.y for v in cell.vs] )
    z = avg( [v.pos.z for v in cell.vs] )
    return vec(x,y,z)

def cell(row,col):
    """return the cell corresponding to row,col"""
    return cellDict[row,col]

def colorFunc(height):
    return vec(0.3-height,0.3 + height, 0.3-height)

# create a Unit class with a smart change method
# (use change to change pos, height, etc., not pos= as with vpython objects)
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
     
        #self.box=boxes[row,col]
        #self.cell = cell(row,col)
        self.pos = self.box.pos
        self.size=1
        self.boxSize = boxSize
        self.height = 0
        self.color=color.magenta
        

    def change(self,color=None, pos=None, height=None, size=None, boxSize=None, rowCol = None, q=None):
        if rowCol is not None:
            #print(self.rowCol,' ->', rowCol)
            self.rowCol = rowCol
            row,col=rowCol
            #self.cell=cell(row,col)
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
            newColor = colorFunc(height)
            self.change( pos=newPos, color =newColor )
            
        
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
    

# make quads and cells and boxes
quads   =  dict()
cellDict = dict()
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
            u = Unit(row,col,q)
            units[row,col] = u

            #cellDict[i//2, j//2] = quads[i,j]
            #cellDict[i//2, j//2].visible=False
            #boxes[i//2, j//2] = b

def swap(rowCol1=(0,0),rowCol2 = (1,1)):
    from copy import copy
    u1 = units[rowCol1]
    u0 = units[rowCol2]    

    #swap critical properties
    u1.q,  u0.q  =  u0.q,    u1.q
    u1.rowCol, u0.rowCol = u0.rowCol, u1.rowCol

    #swap using copy for some reason
    u1boxPos = copy(u1.box.pos) 
    u0boxPos = copy(u0.box.pos)
    u0.box.pos = u1boxPos; u0.change(pos=u0boxPos, color=u0.box.color)
    u1.box.pos = u0boxPos; u1.change(pos=u1boxPos, color=u1.box.color)


def swapUnits(u1,u0):
    from copy import copy
    rowCol1 = u1.rowCol
    rowCol2 = u0.rowCol
    
    #swap critical properties
    u1.q,  u0.q  =  u0.q,    u1.q
    u1.rowCol, u0.rowCol = u0.rowCol, u1.rowCol

    #swap using copy for some reason
    u1boxPos = copy(u1.box.pos) 
    u0boxPos = copy(u0.box.pos)
    u0.box.pos = u1boxPos; u0.change(pos=u0boxPos, color=u0.box.color)
    u1.box.pos = u0boxPos; u1.change(pos=u1boxPos, color=u1.box.color)
    

def fixHandles(rowCol1=(0,0),rowCol2 = (1,1)):
    units[rowCol1], units[rowCol2] = units[rowCol2], units[rowCol1]

def swapper(rowCol1=(0,0),rowCol2 = (1,1)):
    swap(       rowCol1, rowCol2)
    fixHandles( rowCol1, rowCol2)
    
def testSwapper():
    u.change(color=color.red)
    u.change(boxSize=0.5)
    for i in range(20):
        swapper()
        sleep(0.5)

#testSwapper()


from random import random
def initLandscape():
    for row in range(Rows):
        for col in range(Cols):
            height= 1 - (2*random())
            color=colorFunc(height)
            units[row,col].change(height=height,color=color, size=random(), boxSize=random()) #use the changemethod

initLandscape()

u00=units[0,0]
u11=units[1,1]

from copy import copy

def swapProps(u00=units[0,0], u11=units[1,1]):
    #THIS WORKS
    tmp = u00.height #also changes color
    u00.change(height=u11.height)
    u11.change(height=tmp)

    tmp = u00.size
    u00.change(size=u11.size)
    u11.change(size=tmp)

    tmp = u00.boxSize
    u00.change(boxSize=u11.boxSize)
    u11.change(boxSize=tmp)


def sliceDict(XorY='X', index=0,  boxMat = units):
    if not boxMat:
        boxMat=dict() #typically these would be boxes. see test()
        boxMat[0,0]=dict(x=0,y=0)
        boxMat[0,1]=dict(x=0,y=0)
        boxMat[1,0]=dict(x=0,y=0)
        boxMat[1,1]=dict(x=0,y=0)
        
    #print(f'SLICEDict:  {rowOrCol} =  {index}')

    if XorY=='X':
        ret = [[k,v] for k,v in boxMat.items() if k[0]== index]   
    else:
        if XorY!='Y':
            raise Exception('ERROR: rowOrCol must be "X" or "Y"')
            return
        ret = [[k,v] for k,v in boxMat.items() if k[1]== index]   

    retDict=dict()
    for k,v in ret:
        retDict[k] = v
    return retDict

for XorY in ['X','Y']:
    for index in range(Cols):

        SD = sliceDict(XorY, index, units)
        Have = list(SD.values())

        metric = [u.height for u in SD.values()]
        print('\n\nmetric', metric)
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
