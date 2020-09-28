import numpy as np
from utils import loadImage, saveImage, showImage

image = loadImage("pictures/128/005.jpeg", greyscale=False)

mask = loadImage("masks/128/circles.png")

originalimage = np.copy(image)

def isMasked(mask, x ,y):
    if mask[y][x] == 0:
        return True
    return False

def isWithinBounds(x, y, width, height):
    if 0 <= x and x < width and y <= 0 and y < height:
        return True
    return False

def manhattanDistance(x1, y1, x2, y2):
    return np.abs(x1-x2) + np.abs(y1-y2)

def FEMLaplace(_image, _mask):

    #Copy the image
    newimage = np.copy(_image)

    width = newimage.shape[0]
    height = newimage.shape[1]

    print(width)
    print(height)

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

            if manhattanDistance(x1, y1, x2, y2) == 1:
                K[m][n] = 2*a

            if np.abs(x1-x2) == 1 and np.abs(y1-y2) == 1:
                K[m][n] = b 

    K = K+K.transpose()+4*c*np.identity(len(siteindex))

    print(K)

    #Construct force vector
    f = np.zeros((len(siteindex),1))

    for k in range(0,len(siteindex)):
        #Find values of neighbouring Dirichlet boundary conditions
        diagonalsum = 0

        x,y = siteindex[k][0],siteindex[k][1]

        if not isMasked(mask, x-1,y-1):
            diagonalsum += newimage[y-1][x-1]
        if not isMasked(mask, x-1,y+1):
            diagonalsum += newimage[y+1][x-1]
        if not isMasked(mask, x+1,y-1):
            diagonalsum += newimage[y-1][x+1]
        if not isMasked(mask, x+1,y+1):
            diagonalsum += newimage[y+1][x+1]

        adjacentsum = 0

        if not isMasked(mask, x,y+1):
            adjacentsum += newimage[y+1][x]
        if not isMasked(mask, x,y-1):
            adjacentsum += newimage[y-1][x]
        if not isMasked(mask, x+1,y):
            adjacentsum += newimage[y][x+1]
        if not isMasked(mask, x-1,y):
            adjacentsum += newimage[y][x-1]

        f[k][0] = -(diagonalsum*b+adjacentsum*2*a)

    print(f)

    #Solve system
    d = np.linalg.solve(K,f)

    print(d)

    for k in range(0,len(siteindex)):
        
        x, y = siteindex[k][0], siteindex[k][1]

        newimage[y][x] = d[k]

    return newimage

restoredimageR = FEMLaplace(image[:,:,0], mask)
restoredimageG = FEMLaplace(image[:,:,1], mask)
restoredimageB = FEMLaplace(image[:,:,2], mask)

restoredimage = np.dstack([restoredimageR,restoredimageG,restoredimageB])

showImage(np.concatenate([originalimage,np.dstack([mask,mask,mask]).astype(np.uint8),restoredimage],axis=1))

'''
a=-1/6
b=-1/3
c=2/3

M = np.array([[4*c,2*a,0,2*a,b,0,0,0,0],
    [2*a,4*c,2*a,b,2*a,b,0,0,0],
    [0,2*a,4*c,0,b,2*a,0,0,0],
    [2*a,b,0,4*c,2*a,0,2*a,b,0],
    [b,2*a,b,2*a,4*c,2*a,b,2*a,b],
    [0,b,2*a,0,2*a,4*c,0,b,2*a],
    [0,0,0,2*a,b,0,4*c,2*a,0],
    [0,0,0,b,2*a,b,2*a,4*c,2*a],
    [0,0,0,0,b,2*a,0,2*a,4*c]],dtype=float)

B1 = 0.2
B2 = 0.2
B3 = 0.2
B4 = 0.2
B5 = 0.2
B6 = 0.4
B7 = 0.6
B8 = 0.8
B9 = 1
B10 = 1
B11 = 1
B12 = 1
B13 = 1
B14 = 0.8
B15 = 0.6
B16 = 0.4

#Note minus sign
f = -np.array([[b*(B1+B3+B15)+2*a*(B2+B16)],
    [b*(B2+B4) + 2*a*(B3)],
    [b*(B3+B5+B7) + 2*a*(B4+B6)],
    [b*(B16+B14) + 2*a*(B15)],
    [0],
    [b*(B6+B8) + 2*a*(B7)],
    [b*(B15+B13+B11) + 2*a*(B14+B12)],
    [b*(B12+B10) + 2*a*(B11)],
    [b*(B7+B9+B11) + 2*a*(B8+B10)]])

print(M)

d = np.linalg.solve(M,f)
print(1-d)
'''

