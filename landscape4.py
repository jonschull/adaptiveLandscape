from vpython import *

#we'll be making a grid of boxes
Rows = 2
Cols = 2

scene.center = vec(Rows, Cols, 0)
scene.height=800
scene.width=800
local_light(pos=vec(100,100,0), color=color.red)
local_light(pos=vec(-100,-100, 0), color=color.blue)

boxSize=0.9 #for "participation boxes" in cells 
boxDepth=0.2

#make vertices
vertices = dict()
def positionVertices():
    for i in range(-1, 2*Rows+1):
        for j in range(-1, 2*Cols+1):
            pos = vec(i,j,0)
            l=label(pos=pos, text = f'v{i}{j}')  
            vertices[i,j] = vertex(pos=pos, initialPos = pos, label=l)
positionVertices()

def avg(lst):
    return sum(lst)/len(lst)

def centroid(cell):
    x = avg( [v.pos.x for v in cell.vs] )
    y = avg( [v.pos.y for v in cell.vs] )
    z = avg( [v.pos.z for v in cell.vs] )
    return vec(x,y,z)

# # make quads and cells and boxes
# quads   = dict()
# cellDict = dict()
# boxes = dict()

# for i in range(2*Rows+1):
#     for j in range( 2*Cols+1):
#         vs=[    vertices[i,j],
#                 vertices[i-1,j],
#                 vertices[i-1,j-1],
#                 vertices[i, j-1]    ]

#         q = quad(vs=vs,
#             texture=textures.rough,
#             shininess=0,)
#         q.label = label(pos=centroid(q), text=f'Q{i}{j}', color=color.yellow, visible=True)

#         quads[i,j] = q

#         if i%2 and j%2:
#             #cellDict[i//2, j//2] = quads[i,j]
#             #cellDict[i//2, j//2].visible=False

#             boxpos = centroid(quads[i,j])
#             b =box(pos = boxpos,
#                    size= vec(boxSize,boxSize,boxDepth),
#                    label=label(pos=boxpos + vec(0,-0.2,0), text=f'B{i}{j}',  color=color.green) )
#             boxes[i//2, j//2] = b
# 1/0

def cell(row,col):
    """return the cell corresponding to row,col"""
    return cellDict[row,col]

def colorFunc(height):
    return vec(0.3-height,0.3 + height, 0.3-height)

# create a Unit class with a smart change method
# (use change to change pos, height, etc., not pos= as with vpython objects)
class Unit:
    def __init__(self, row,col,q):
        self.rowCol=(row,col)
        self.q = q
        boxPos = centroid(q)
        self.box =box(  pos = boxPos,
                        size= vec(boxSize,boxSize,boxDepth),
                        label=label(pos=boxPos + vec(0,-0.2,0), text=f'B{i}{j}',  color=color.green) )
     
        #self.box=boxes[row,col]
        #self.cell = cell(row,col)
        self.pos = self.box.pos
        self.size=1
        self.boxSize = boxSize
        self.height = 0
        self.color=color.magenta
        
    def change(self,color=None, pos=None, height=None, size=None, boxSize=None, rowCol = None, q=None):
        if rowCol is not None:
            print(self.rowCol,' ->', rowCol)
            #self.rowCol = rowCol
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
            # capture vertices relative to box
            for i in range(4):
                print('XXX', self.q.vs[i].pos,self.box.pos)
                deltaVs[i] = self.q.vs[i].pos - self.box.pos
                
            self.pos = pos
            # move box
            self.box.pos = pos
            
            #reposition vertices relative to box
            for i in range(4):
                self.q.vs[i].pos -= deltaVs[i]

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
            self.boxSize = self.boxSize * vec(size,size,boxDepth)
            self.box.size = self.boxSize
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
        q.label = label(pos=centroid(q), text=f'Q{i}{j}', color=color.yellow, visible=True)

        quads[i,j] = q

        if i%2 and j%2:
            row, col = i//2, j//2
            print(row,col)
            q = quads[i,j]
            q.visible=False
            u = Unit(row,col,q)
            units[row,col] = u

            #cellDict[i//2, j//2] = quads[i,j]
            #cellDict[i//2, j//2].visible=False
            #boxes[i//2, j//2] = b


def swapper(rowCol1=(0,0),rowCol2 = (1,1)):
    #SWAPPER    
    from copy import copy
    u1 = units[rowCol1]
    u0 = units[rowCol2]    

    #swap critical properties
    u1.q,  u0.q  =  u0.q,    u1.q
    u1.rowCol, u0.rowCol = u0.rowCol, u1.rowCol

    #swap using copy for some reason
    u1boxPos = copy(u1.box.pos) 
    u0boxPos = copy(u0.box.pos)
    u0.box.pos = u1boxPos; u0.change(color=u0.box.color)
    u1.box.pos = u0boxPos; u1.change(color=u1.box.color)
    
    #swap handles
    units[rowCol1], units[rowCol2] = units[rowCol2], units[rowCol1]  
    
def testSwapper():
    u.change(color=color.red)
    u.change(boxSize=0.5)
    for i in range(2):
        swapper()
        sleep(0.5)

testSwapper()
u=units[0,0]
u.change(color=color.yellow)
#u.change(height=0.5)

#u1.rowCol, u0.rowCol = u0.rowCol, u1.rowCol

#units[0,0], units[1,1] = u1,u0



# 1/0

# #make the units
# units=dict()
# for row in range(Rows):
#     for col in range(Cols):
#         units[row,col]= Unit(row,col)

from random import random
def initLandscape():
    for row in range(Rows):
        for col in range(Cols):
            height= 1 - (2*random())
            color=colorFunc(height)
            units[row,col].change(height=height,color=color) #use the changemethod

#initLandscape()

# def redraw():
#     for row in range(Rows):
#         for col in range(Cols):
#            u =  units[row,col]
#            units[row,col].change(
#                rowCol  =u.rowCol,
#                pos      = u.pos, 
#                height   = u.height.z,
#                color    = u.color,
#                boxSize  = u.boxSize
#                ) #use the changemethod


# def resetVertices():
#     for v in vertices: 
#         vertices[v].pos = vertices[v].initialPos
#         initLandscape()


# # scene.caption="""
# # <h3>caption</h3>
# # Each column of squares represents a group. 
# # Each row of squares represents a question.
# # For each square<ul>
# # <li> The altitude/color of each square reflects agreement.
# # <li> The size of each square represents the number of people who voted.
# # <li> The thickness of the black outline of each square represents the number of people who passed.
# # </ul>

# # This where detail would be shown on hover.
# # <ul><li>question
# # <li>Agree
# # <li>Disagree
# # <li>Pass
# # </ul>

# # """

# from bubblesort2D import sortRectangle

# def myMetricFunc(listOfCells):
#     """ this is MY metric function 
#     """
#     ret = [u.height.z for u in listOfCells]
#     return ret

# u=units[0,0]
# sortRectangle(units, Rows,Cols, metricFunc=myMetricFunc)
# sleep(0.5)
# redraw()