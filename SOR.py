# -*- coding: utf-8 -*-
"""
Takes the mask indicies and values from neighbours and returns a list consisting values for the points in the mask.
 repeates untill sufficiently restored.


"""

import numpy as np
from random import randint
def SOR(maskIndex, neighbours,n,omega): 
    maximumIndex=(maskIndex[-1]+1)
    restored=np.zeros(maximumIndex) # restored consists of index for the interior point restored and the second list is the values for these points
    for a in range(len(maskIndex)):     #assigning random values
        restored[a]=randint(1,255)
        
        

    for o in range(n):
        for t in range(len(maskIndex)):
            Closest=[]
            for i in range(len(neighbours[t][0])):
                Closest.append(restored[neighbours[t][0][i]])
            for p in range(len(neighbours[t][1])):
                Closest.append(neighbours[t][1][p])
            restored[t]=((1-omega)*restored[t]+(omega/(4))*sum(Closest))    
    restored = [x for x in restored if x !=0]
    for l in range(len(restored)):
      if restored[l]<1:
          restored[l]=1
          
    return restored 

def RestoreIndex(imageMatrix,restored,maskIndex):
    a=0
    for i in maskIndex:
        imageMatrix[i]=restored[a]
        a=a+1
    return imageMatrix


        