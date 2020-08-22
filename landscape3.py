from vpython import *

Rows = 3
Cols = 3
scene.center = vec(Rows, Cols, 0)
local_light(pos=vec(100,100,0), color=color.red)
local_light(pos=vec(-100,-100, 0), color=color.blue)

#make vertices
vertices = dict()
for row in range(-1, 2*Rows+1):
    for col in range(-1, 2*Cols+1):
        vertices[row,col] = vertex(pos=vec(row,col,0))
        #label(border=0, opacity=0, pos=vec(row,col,0), text=str(vec(row,col,0)))

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

def modCell(row=0,col=0, height=0.5,color=vec(1,1,1)):
    target = cells[rowcol(row,col)]
    for i,v in enumerate(target.vs):
        target.vs[i].pos.z = height
        target.vs[i].color = color
        target.emissive=False

#test
def test():
    for row in range(Rows):
        print()
        for col in range(Cols):
            height=(row - col)/((Rows+Cols)/2)
            color=vec(-height,0.3 + height, height)
            modCell(row,col, height = height, color=color)
            print(height, end=' ')
test()
