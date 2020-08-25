from time import sleep
from random import random
from vpython import box,vec,label

def bubblesort( A, Bs, axis='x' ):
  """A is the metric, Bs is list of Boxes """
  for i in range( len( A ) ):
    for k in range( len( A ) - 1, i, -1 ):
      if ( A[k] < A[k - 1] ):
        #swap( A, k, k - 1 )
        A[k], A[k-1]   = A[k-1],A[k]
        Bs[k],Bs[k-1]  = Bs[k-1],Bs[k] 
        if axis == 'x':
            Bs[k].pos.x   = k
            Bs[k-1].pos.x = k-1
        else:
            Bs[k].pos.y   = k
            Bs[k-1].pos.y = k-1
        sleep(0.001)
    #print(A)

def sliceDict(rowOrCol='row', index=0,  boxMat = None):
    if not boxMat:
        boxMat=dict() #typically these would be boxes. see test()
        boxMat[0,0]=dict(x=0,y=0)
        boxMat[0,1]=dict(x=0,y=0)
        boxMat[1,0]=dict(x=0,y=0)
        boxMat[1,1]=dict(x=0,y=0)
        
    #print(f'SLICEDict:  {rowOrCol} =  {index}')

    #col with index 0 means all cells are X=0
    if rowOrCol=='col':
        ret = [[k,v] for k,v in boxMat.items() if k[0]== index]   
    else:
        if rowOrCol!='row':
            raise Exception('ERROR: rowOrCol must be "row" or "col"')
            return
        ret = [[k,v] for k,v in boxMat.items() if k[1]== index]   

    retDict=dict()
    for k,v in ret:
        retDict[k] = v
    return retDict


def test():
    Rows=20
    Cols=20
    #make boxMat: a dictionary[row,col] of boxes
    boxMat = dict()
    for row in range(Rows):
        for col in range(Cols):
            r=random()
            boxMat[row,col] = box(pos = vec(row,col,0), color=vec(r,1-r,0))


    #sort cols
    for col in range(Cols):
        listOfCells = list(sliceDict('col', col, boxMat).values())
        metric = [c.color.x for c in listOfCells]
        bubblesort(metric, listOfCells, axis='y')
        #update boxMat
        for cell in listOfCells:
            boxMat[cell.pos.x,cell.pos.y] = cell

    #sort rows
    for row in range(Rows):
        listOfCells = list(sliceDict('row', row, boxMat).values())
        metric = [c.color.x for c in listOfCells]
        bubblesort(metric, listOfCells, axis='x')
        #update boxMat
        for cell in listOfCells:
            boxMat[cell.pos.x,cell.pos.y] = cell

test()

