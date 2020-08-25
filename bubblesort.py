from time import sleep
def bubblesort( A ):
  for i in range( len( A ) ):
    for k in range( len( A ) - 1, i, -1 ):
      if ( A[k] < A[k - 1] ):
        #swap( A, k, k - 1 )
        A[k], A[k-1]   = A[k-1],A[k]
        Bs[k],Bs[k-1]  = Bs[k-1],Bs[k] 
        Bs[k].pos.x = k
        Bs[k-1].pos.x = k
        sleep(0.1)

  print(A)
  for b in range(len(Bs)):
    Bs[b].pos.x = b
  

from random import random
A=[round(10*random()) for x in range(10)]  
print(A)

from vpython import box,vec,label

Bs=[]
for i,a in enumerate(A):
  B=box(pos = vec(i,0,0), color=vec(a/10,1-a/10,0))
  #label(pos=B.pos, text=str((i,a)))
  Bs.append(B)
bubblesort(A)