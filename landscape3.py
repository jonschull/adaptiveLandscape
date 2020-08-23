from vpython import *

Rows = 3
Cols = 3
scene.center = vec(Rows, Cols, 0)
local_light(pos=vec(100,100,0), color=color.red)
local_light(pos=vec(-100,-100, 0), color=color.blue)

#make vertices
vertices = dict()

def positionVertices():
    for row in range(-1, 2*Rows+1):
        for col in range(-1, 2*Cols+1):
            vertices[row,col] = vertex(pos=vec(row,col,0), initialPos = vec(row,col,0))
            #label(border=0, opacity=0, pos=vec(row,col,0), text=str(vec(row,col,0)))
positionVertices()

# make quads 
quads=dict()
cells=[]
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
            cells.append(quads[row,col])

def rowcol(row=0,col=0):
    "integer corresonding to row,col"
    return row * Cols + col

def cell(row,col):
    return cells[rowcol(row,col)]

def heightAndColor(row=0,col=0, height=999,color=None):
    target = cell(row,col)
    for i,v in enumerate(target.vs):
        if height!=999:
            target.vs[i].pos.z = height
        if color:
            target.vs[i].color = color
    target.visible=False
    target.cellHeight = height
    target.cellColor = color

def initLandscape():
    for row in range(Rows):
        print()
        for col in range(Cols):
            height=(col - row)/((Rows+Cols)/3)
            color=vec(-height,0.3 + height, height)
            heightAndColor(row,col, height = height, color=color)
initLandscape()

def resetVertices():
    for v in vertices: 
        vertices[v].pos = vertices[v].initialPos
        initLandscape()

def moveCells(deltaX=0,deltaY=0):
    for row in range(Rows):
        for col in range(Cols):
            target = cell(row,col)
            for i in range(4):
                target.vs[i].pos.x += deltaX
                target.vs[i].pos.y += deltaY
#moveCells(2,2)

def wideAndLong(row=0,col=0, wide=0.5, long=0.5):
    target = cell(row,col)
    for i,v in enumerate(target.vs):
        print(target.vs[i].pos.x,target.vs[i].pos.y)
        TR, TL, BL, BR = 0,1,2,3 #T is top, B is Bottom
    target.vs[TR].pos.x = target.vs[TL].pos.x + wide
    target.vs[BR].pos.x = target.vs[BL].pos.x + wide
    target.vs[TR].pos.y = target.vs[BR].pos.y + long
    target.vs[TL].pos.y = target.vs[BL].pos.y + long
    print()
    for i,v in enumerate(target.vs):
        print(target.vs[i].pos.x,target.vs[i].pos.y)
    
def shrinkCells(wide=0.5,tall=0.5):
    for row in range(Rows):
        for col in range(Cols):
            wideAndLong(row,col, wide,tall)
