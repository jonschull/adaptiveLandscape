from vpython import compound, quad,color,vertex,vec, label, scene

from pprint import pprint


def Quad():
    """how to make a quad"""
    a = vertex( pos=vec(0,0,0),color=color.red )
    b = vertex( pos=vec(1,0,0),color=color.blue )
    c = vertex( pos=vec(1,1,0),color=color.green )
    d = vertex( pos=vec(0,1,0),color=color.yellow )
    return quad( vs=[a,b,c,d] )

#q = Quad()
#Q=compound(q)

Rows = 3
Cols = 3
scene.center = vec(Rows, Cols, -50)
scene.width = scene.height = 800

vertexes = dict()
for row in range(-1, 2*Rows+1):
    for col in range(-1, 2*Cols+1):
        vertexes[row,col] = vec(row,col,-0)

labels=[]
for k,v in vertexes.items():
    row,col = k
    labels.append(
        label(pos= vec(row,col,0), 
               text=str(k), 
               box = False,
               opacity=0 )
    )


def vertices(R=0,C=0):
    lowerRight = (2*R+1, 2*C)
    upperRight = (2*R+1, 2*C + 1)
    upperLeft = (2*R, 2*C + 1)
    lowerLeft = (2*R, 2*C)
    
    return [ vertex(pos = vertexes[lowerRight], color=color.red), 
             vertex(pos = vertexes[upperRight], color=color.blue), 
             vertex(pos = vertexes[upperLeft], color=color.green), 
             vertex(pos = vertexes[lowerLeft], color=color.yellow) ]



cells = dict()
for row in range(Rows):
    for col in range(Cols):
        cells[row,col] = quad(vs = vertices(row,col))

#make lefties
for row,col in cells.keys():
    cell = cells[row,col]
    #vertices of the cell
    ll,lr,ur,ul = cell.vs
    #corners of the cell to be
    UR = ul
    LR = ll
    LL = vertex(color=color.white, pos = vec(0,0,0))
    UL = vertex(color=color.white, pos=vec(1,1,0))
    q = quad(vs=[LL,LR,UR,UL])