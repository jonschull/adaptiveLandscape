#!/usr/bin/env python
from vpython import quad,color,vertex,vec, arrow

red=color.red
green=color.green
blue=color.blue
yellow=color.yellow
black=color.black
gray=vec(0.2,0.2,0.2)

def showQuad():
    """how to make a quad"""
    a = vertex( pos=vec(0,0,0),color=red )
    b = vertex( pos=vec(1,0,0),color=blue )
    c = vertex( pos=vec(1,1,0),color=green )
    d = vertex( pos=vec(0,1,0),color=yellow )
    quad( vs=[a,b,c,d] )

def showVecs():
    """how to find the v3 between v1 and v2"""
    v1 = vec(0,0,1,)
    v2 = vec(0,1,2)
    v3 = v1 + v2
    arrow(axis=v1, pos=vec(0,0,0), color=green)
    arrow(axis=v2,   pos=vec(0,0,0), color=green)
    arrow(axis=v3, pos=vec(0,0,0), color=yellow)

def square(row=0, col=0, alt=0, color=blue):
    """make a flat square"""
    r,c,a = -row, col, alt
    vs = [  vertex(pos = vec(c,  r,   a), color=red),
            vertex(pos = vec(c,  r+1, a), color=blue),
            vertex(pos = vec(c+1,r+1, a), color=green),
            vertex(pos = vec(c+1,r,   a), color=yellow)  ]
    
#    vs = [  vertex(pos = vec(c,  r,   a), color=gray),
#            vertex(pos = vec(c,  r+1, a), color=gray),
#            vertex(pos = vec(c+1,r+1, a), color=gray),
#            vertex(pos = vec(c+1,r,   a), color=gray)  ]

    return quad(vs=vs)

def makePatches(numRows=5, numCols=5):
    
    patches=[]
    numRows=numCols=5
    for row in range(-1, numRows + 1): # 1,-1 for margin row
        R=[]
        for col in range(-1, numCols +1): #-1, 1 for margin col
            R.append(square(row=row,col=col))
        patches.append(R)
    return patches

patches = makePatches()    


def info(patches=patches):
    rows = len(patches)
    cols = len(patches[0])
    lastrow = len(patches) - 1
    lastcol= len(patches[lastrow]) -1
    
    if lastcol<cols: #time to move to next row
        nextcell = (lastrow, lastcol+1)
    else:
        nextcell = (lastrow+1, 0)
    
    return dict(rows=rows,
                cols=cols,
                lastrow=lastrow,
                lastcol=lastcol,
                nextcell=nextcell)


print(info(patches))

from copy import copy, deepcopy

def changePatch(row=1,col=1, alt=0.5):
    target = patches[row][col]
    target.v0.pos = patches[row-1][col].v3.pos;   
    target.v1.pos = patches[row-1][col-1].v3.pos; 
    target.v2.pos = patches[row][col-1].v3.pos;   
    target.v3.pos = target.v3.pos;                
    target.v3.pos.z = alt
    target.v0.color = color.white 
    target.v1.color = color.orange
    target.v2.color = color.magenta 
    target.v3.color = vec(0.5,0.5,0.5) #gray is broken
    patches[row][col]=target

def test1():
    changePatch(1,1,0.5)
    changePatch(1,2,-0.5)
    changePatch(2,1,-0.5)
    changePatch(2,2,0)
    changePatch(2,3,0.5)
    changePatch(1,3,0)

#test1()

rows, cols, lastrow, lastcol, nextcell = (info().values())

def test2():

    i=0.0
    for row in range(rows):
        for col in range(cols-1):
            i = i + 0.3
            changePatch(row,col,i)
