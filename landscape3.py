from vpython import compound, quad,color,vertex,vec, label, scene

def Quad():
    """how to make a quad"""
    a = vertex( pos=vec(0,0,0),color=color.red )
    b = vertex( pos=vec(1,0,0),color=color.blue )
    c = vertex( pos=vec(1,1,0),color=color.green )
    d = vertex( pos=vec(0,1,0),color=color.yellow )
    return quad( vs=[a,b,c,d] )


Rows = 3
Cols = 3
scene.center = vec(Rows, Cols, 0)
#scene.width = scene.height = 800

#make vertices
vertices = dict()
for row in range(-1, 2*Rows+1):
    for col in range(-1, 2*Cols+1):
        vertices[row,col] = vertex(pos=vec(row,col,-0))

#make labels from vertices
# labels=[]
# for k,v in vertices.items():
#     row,col = k
#     labels.append(
#         label(pos= vertices[row,col].pos, 
#                text=str(k), 
#                box = False,
#                opacity=0 )
#     )


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
            ])
        if row%2 and col%2:
            quads[row,col].v0.color=color.blue
            quads[row,col].v1.color=color.blue
            quads[row,col].v2.color=color.blue
            quads[row,col].v3.color=color.blue
            cells.append(quads[row,col])

def modCell(row=0,col=0, height=1):
    target = cells[0]
    for i,v in enumerate(target.vs):
        target.vs[i].pos.z = height
        target.vs[i].color = vec(0,height, 0)
        
modCell()

