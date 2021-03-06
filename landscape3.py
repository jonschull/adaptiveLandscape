from vpython import *

Rows = 5
Cols = 5
scene.center = vec(Rows, Cols, 0)
local_light(pos=vec(100,100,0), color=color.red)
local_light(pos=vec(-100,-100, 0), color=color.blue)

boxSize=0.9 #for "participation boxes" in cells 
boxDepth=0.2

#make vertices
vertices = dict()
def positionVertices():
    for row in range(-1, 2*Rows+1):
        for col in range(-1, 2*Cols+1):
            vertices[row,col] = vertex(pos=vec(row,col,0), initialPos = vec(row,col,0))
positionVertices()


def avg(lst):
    return sum(lst)/len(lst)

def pos(cell):
    x = avg( [v.pos.x for v in cell.vs] )
    y = avg( [v.pos.y for v in cell.vs] )
    z = avg( [v.pos.z for v in cell.vs] )
    return vec(x,y,z)

# make quads and cells and boxes
quads   = dict()
cellDict = dict()
boxes = dict()

for row in range(2*Rows+1):
    for col in range( 2*Cols+1):
        quads[row,col] = quad(vs=[
                vertices[row,col],
                vertices[row-1,col],
                vertices[row-1,col-1],
                vertices[row, col-1]
            ], 
            texture=textures.rough,
            shininess=0)
        if row%2 and col%2:
            cellDict[row//2, col//2] = quads[row,col]
            cellDict[row//2, col//2].visible=False
            boxes[row//2, col//2] = box(
                                        pos = pos(quads[row,col]),
                                        size= vec(boxSize,boxSize,boxDepth)
                                        )

def cell(row,col):
    """return the cell corresponding to row,col"""
    return cellDict[row,col]

def colorFunc(height):
    return vec(0.3-height,0.3 + height, 0.3-height)

# create a Unit class with a smart change method
# (use change to change pos, height, etc., not pos= as with vpython objects)
class Unit:
    def __init__(self, row,col):
        self.box=boxes[row,col]
        self.cell = cell(row,col)
        self.pos = self.box.pos
        self.size=1
        self.boxSize = boxSize

    def change(self,color=None, pos=None, height=None, size=None, boxSize=None):
        if color is not None:
            self.box.color=color
            for i in range(4):
                self.cell.vs[i].color=color
            
        if pos is not None:
            oldPos = self.pos
            deltaPos = oldPos - pos
            self.pos = pos
            self.box.pos = pos
            for i in range(4):
                self.cell.vs[i].pos -= deltaPos

        if height is not None:
            newPos = vec(
                self.pos.x,
                self.pos.y,
                height)
            newColor = colorFunc(height)
            self.change( pos=newPos, color =newColor )
        
        if boxSize is not None: #boxsize is relative to cell size; 1 means no visible frame
            self.boxSize=boxSize
            self.box.size = self.boxSize * vec(self.size,self.size,0.2)
            

        if size is not None: # voters
            self.size=size
            TR, TL, BL, BR = 0,1,2,3 #T is top, B is Bottom
            target=self.cell
            wide=long=size
            target.vs[TR].pos.x = target.vs[TL].pos.x + wide
            target.vs[BR].pos.x = target.vs[BL].pos.x + wide
            target.vs[TR].pos.y = target.vs[BR].pos.y + long
            target.vs[TL].pos.y = target.vs[BL].pos.y + long
            self.boxSize = self.boxSize * vec(size,size,boxDepth)
            self.box.size = self.boxSize
            newPos= target.vs[BL].pos + vec(size/2, size/2,0)
            self.pos = newPos
            self.box.pos = newPos
    


#make the units
units=dict()
for row in range(Rows):
    for col in range(Cols):
        units[row,col]= Unit(row,col)

def initLandscape():
    for row in range(Rows):
        for col in range(Cols):
            height=(col - row)/((Rows+Cols)/3)
            color=colorFunc(height)
            units[row,col].change(height=height,color=color) #use the changemethod

initLandscape()

def resetVertices():
    for v in vertices: 
        vertices[v].pos = vertices[v].initialPos
        initLandscape()


# scene.caption="""
# <h3>caption</h3>
# Each column of squares represents a group. 
# Each row of squares represents a question.
# For each square<ul>
# <li> The altitude/color of each square reflects agreement.
# <li> The size of each square represents the number of people who voted.
# <li> The thickness of the black outline of each square represents the number of people who passed.
# </ul>

# This where detail would be shown on hover.
# <ul><li>question
# <li>Agree
# <li>Disagree
# <li>Pass
# </ul>

# """


u=units[0,0]
u.change(size=0.5,boxSize=0.5)
