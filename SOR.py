# -*- coding: utf-8 -*-
"""
Takes the mask indicies and values from neighbours and returns a list consisting values for the points in the mask.
 repeates untill sufficiently restored.


"""

import numpy as np
from random import randint
def SOR(maskIndex, neighbours,n,omega): 
    iterations=np.linspace(1,n,n)
    maximumIndex=len(maskIndex)
    restored=np.zeros(maximumIndex) # restored consists of index for the interior point restored and the second list is the values for these points
    rho=0.9
    h=1/n
    for a in range(len(maskIndex)):     #assigning random values
        restored[a]=randint(1,255)
        
        
# This thing never checks if they have been used previously.
# it simply uses the values from the restored list which are initialised and then updated.

    
    for i in iterations:  
        for t in range(len(maskIndex)):
            if len(neighbours[t][0]) > 3:
                restored[t]=(1-omega)*(restored[t])*(omega/4)*((restored[(neighbours[t][0][0])])+(restored[(neighbours[t][0][1])])+(restored[(neighbours[t][0][2])])+(restored[(neighbours[t][0][3])])-rho*h**2)                
            elif len(neighbours[t][0]) > 2: 
                restored[t]=(1-omega)*(restored[t])*(omega/3)*((restored[(neighbours[t][0][0])])+(restored[(neighbours[t][0][1])])+(restored[(neighbours[t][0][2])])+sum(neighbours[t][1])-rho*h**2)            
            elif len(neighbours[t][0]) > 1: 
                restored[t]=(1-omega)*(restored[t])*(omega/2)*((restored[(neighbours[t][0][0])])+(restored[(neighbours[t][0][1])])+sum(neighbours[t][1])-rho*h**2)            
            elif len(neighbours[t][0]) > 0:
                restored[t]=(1-omega)*(restored[t])*(omega/1)*((restored[(neighbours[t][0][0])])+sum(neighbours[t][1])-rho*h**2)
            else:
                break
                
 #   restored = [x for x in restored if x !=0]# this is merely used for a check and should be removed later.
    return restored 

def RestoreIndex(imageMatrix,restored,maskIndex):
    for i in maskIndex:
        imageMatrix[i]=restored[i]
    return imageMatrix


        