from time import sleep
from random import random
from vpython import box,vec,label

def bubblesort( A, Bs, axis='x' ):
  """A is the metric, Bs is list of Boxes """
  for i in range( len( A ) ):
    for k in range( len( A ) - 1, i, -1 ):
      if ( A[k] < A[k - 1] ):
        
        #swap!
        A[k],  A[k-1]   =  A[k-1],  A[k]
        Bs[k], Bs[k-1]  =  Bs[k-1], Bs[k] 
        
        #but changing handles doesn't change the objects 
        #so we also swap positions on the appropriate axis
        if axis == 'x':
            Bs[k].pos.x, Bs[k-1].pos.x = Bs[k-1].pos.x, Bs[k].pos.x
        else:
            Bs[k].pos.y, Bs[k-1].pos.y = Bs[k-1].pos.y, Bs[k].pos.y

        #Note: since B is local we will be changing the boxMat indices outside
        sleep(0.0001)

def sliceDict(RowOrCol='Row', index=0,  boxMat = None):
    if not boxMat:
        boxMat=dict() #typically these would be boxes. see test()
        boxMat[0,0]=dict(x=0,y=0)
        boxMat[0,1]=dict(x=0,y=0)
        boxMat[1,0]=dict(x=0,y=0)
        boxMat[1,1]=dict(x=0,y=0)
        
    #print(f'SLICEDict:  {rowOrCol} =  {index}')

    #col with index 0 means all cells are X=0
    if RowOrCol=='Col':
        ret = [[k,v] for k,v in boxMat.items() if k[0]== index]   
    else:
        if RowOrCol!='Row':
            raise Exception('ERROR: rowOrCol must be "row" or "col"')
            return
        ret = [[k,v] for k,v in boxMat.items() if k[1]== index]   

    retDict=dict()
    for k,v in ret:
        retDict[k] = v
    return retDict

def metricFunc(listOfCells):
    return [c.color.x for c in listOfCells]

def sortSlice(RowOrCol,RowOrColIndex, boxMat, metricFunc=metricFunc):
    AxisForRowOrCol = dict(Row= 'x',
                           Col= 'y')

    listOfCells = list(sliceDict(RowOrCol, RowOrColIndex, boxMat).values())
    originalKeys= list(sliceDict(RowOrCol, RowOrColIndex, boxMat).keys())
    metric = metricFunc(listOfCells)
    bubblesort(metric, listOfCells, axis= AxisForRowOrCol[ RowOrCol ] )
    for i,key in enumerate(originalKeys):
        boxMat[ originalKeys[i] ] = listOfCells[i]
        
def sortSlices(boxMat, RowOrCol='Row'):
    global Rows, Cols
    global paramDict

    IndicesForRowOrCol = dict(Row= range(Rows),
                              Col= range(Cols))
    
    for RowOrColIndex in IndicesForRowOrCol[ RowOrCol ]:
        sortSlice(RowOrCol,RowOrColIndex, boxMat, metricFunc)




Rows=10
Cols=20

def makeBoxMat(Rows=Rows,Cols=Cols):
    boxMat = dict()
    for row in range(Rows):
        for col in range(Cols):
            r=random()
            boxMat[row,col] = box(pos = vec(row,col,0), color=vec(r,1-r,0))
    return boxMat


boxMat=makeBoxMat()

def sortRectangle(Rows=Rows,Cols=Cols, boxMat=boxMat, metricFunc=metricFunc):
    for _ in [1,2]: #second pass is needed to mop up rows
        for i in range(max(Rows,Cols)):
            if i<Cols: sortSlice('Row', i, boxMat, metricFunc)
            if i<Rows: sortSlice('Col', i, boxMat, metricFunc)

sortRectangle(Rows,Cols,boxMat, metricFunc)

