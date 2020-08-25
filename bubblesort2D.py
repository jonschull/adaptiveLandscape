from time import sleep
from random import random
from vpython import box,vec,label

def bubblesort( A, Bs, axis='x' ):
  """A is the metric, Bs are Boxes in rows"""
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
        sleep(0.1)
    print(A)

  

def oneD():
    A=[round(10*random()) for x in range(10)]  
    Bs=[]
    for i,a in enumerate(A):
        #position left to right, green to red
        B=box(pos = vec(i,0,0), color=vec(a/10,1-a/10,0))
        Bs.append(B)

    bubblesort(A,Bs, axis='x')

#oneD()

Rows=10
Cols=10
boxMat = dict()
for row in range(Rows):
    for col in range(Cols):
        r=random()
        boxMat[row,col] = box(pos = vec(row,col,0), color=vec(r,1-r,0))

def sliceDict(rowOrCol='row', index=0,  mat = boxMat):
    print(f'SLICE:  {rowOrCol} =  {index}')

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



sliceDict()


