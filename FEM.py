import numpy as np
from utils import loadImage, saveImage, showImage, discrepancyScore, makeMask

#image = loadImage("pictures/128/005.jpeg", greyscale=False)

#mask = loadImage("masks/128/circles.png")

#originalimage = np.copy(image)

def isMasked(mask, x ,y):
    if mask[y][x] == 0:
        return True
    return False

def isWithinBounds(x, y, width, height):
    if 0 <= x and x < width and y <= 0 and y < height:
        return True
    return False

def FEMLaplace(_image, _mask):
    #Copy the image
    newimage = np.copy(_image)

    width = newimage.shape[0]
    height = newimage.shape[1]

    #Site indexing
    siteindex = []

    for y in range(0,height):
        for x in range(0,width):
            interesting = False
            
            if isMasked(_mask, x, y):
                siteindex.append((x, y))

    #construct stiffness matrix
    K = np.zeros((len(siteindex),len(siteindex)))

    a=-1/6
    b=-1/3
    c=2/3

    for m in range(0,len(siteindex)):
        for n in range(0, m):
            x1, y1 = siteindex[m][0], siteindex[m][1]
            x2, y2 = siteindex[n][0], siteindex[n][1]

            if np.abs(x1-x2) + np.abs(y1-y2) == 1:
                K[m][n] = 2*a

            if np.abs(x1-x2) == 1 and np.abs(y1-y2) == 1:
                K[m][n] = b 

    K = K+K.transpose()+4*c*np.identity(len(siteindex))

    #Construct force vector
    f = np.zeros((len(siteindex),1))

    for k in range(0,len(siteindex)):
        #Find values of neighbouring Dirichlet boundary conditions
        diagonalsum = 0

        x,y = siteindex[k][0],siteindex[k][1]

        if not isMasked(_mask, x-1,y-1):
            diagonalsum += newimage[y-1][x-1]
        if not isMasked(_mask, x-1,y+1):
            diagonalsum += newimage[y+1][x-1]
        if not isMasked(_mask, x+1,y-1):
            diagonalsum += newimage[y-1][x+1]
        if not isMasked(_mask, x+1,y+1):
            diagonalsum += newimage[y+1][x+1]

        adjacentsum = 0

        if not isMasked(_mask, x,y+1):
            adjacentsum += newimage[y+1][x]
        if not isMasked(_mask, x,y-1):
            adjacentsum += newimage[y-1][x]
        if not isMasked(_mask, x+1,y):
            adjacentsum += newimage[y][x+1]
        if not isMasked(_mask, x-1,y):
            adjacentsum += newimage[y][x-1]

        f[k][0] = -(diagonalsum*b+adjacentsum*2*a)

    #Solve system for the 'displacement vector', i.e. the pixel values
    d = np.linalg.solve(K,f)

    for k in range(0,len(siteindex)):
        x, y = siteindex[k][0], siteindex[k][1]
        newimage[y][x] = d[k]

    return newimage

#restoredimageR = FEMLaplace(image[:,:,0], mask)
#restoredimageG = FEMLaplace(image[:,:,1], mask)
#restoredimageB = FEMLaplace(image[:,:,2], mask)

#restoredimage = np.dstack([restoredimageR,restoredimageG,restoredimageB])

#showImage(np.concatenate([originalimage,np.dstack([mask,mask,mask]).astype(np.uint8),restoredimage],axis=1))

#DSMask = makeMask("masks/128/circles.png") #Need the mask site index list
#scoreR = discrepancyScore(originalimage[:,:,0], restoredimageR, DSMask[1])
#scoreG = discrepancyScore(originalimage[:,:,1], restoredimageG, DSMask[1])
#scoreB = discrepancyScore(originalimage[:,:,2], restoredimageB, DSMask[1])


#scoreTot = (scoreR + scoreG + scoreB)/3
#print("Average discrepancy score = " + str(scoreTot))


