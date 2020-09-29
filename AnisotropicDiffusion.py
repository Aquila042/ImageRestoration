from utils import loadImage, showImage
import numpy as np

#Diffusivity constant
K = 1

#Diffusivity function
#def g(norm_laplacian_squared):
#    return np.exp(-norm_laplacian_squared/(K**2))

def g(x):
    return 1/(1+x/(K**2))**2

#Initial function
image = loadImage("pictures/32/discretegradient.png").astype(np.float64)
mask = loadImage("masks/32/smallsquares.png").astype(np.float64)

u0 = np.zeros((image.shape[0],image.shape[1]))

for x in range(0,image.shape[1]):
    for y in range(0,image.shape[0]):
        if mask[y][x] < 128:
            u0[y][x] = np.random.randint(255)
        else:
            u0[y][x] = image[y][x]

#Indexing helper, effectively yields the Neumann boundary conditions, since out-of-bounds pixels are copies of the within-bound closest one
def get_u(u,x,y):
    if x < 0:
        return u[y][0]
    if x > u.shape[1]-1:
        return u[y][x-1]
    if y < 0:
        return u[0][x]
    if y > u.shape[0]-1:
        return u[y-1][x]
    return u[x][y]

#Function for calculating g-matrix
def g_matrix(u):
    G = np.zeros(u.shape)
    for x in range(0,u.shape[1]):
        for y in range(0,u.shape[0]):
            norm_laplacian_squared = max((get_u(u,x+1,y)-get_u(u,x,y))*(get_u(u,x,y)-get_u(u,x-1,y)),0) 
            + max((get_u(u,x,y+1)-get_u(u,x,y))*(get_u(u,x,y)-get_u(u,x,y-1)),0) 
            #norm_laplacian_squared = ((get_u(u,x+1,y)-get_u(u,x-1,y))/2)**2+((get_u(u,x,y+1)-get_u(u,x,y-1))/2)**2
            G[x][y] = g(norm_laplacian_squared)
    
    return G

'''
G0 = g_matrix(u0)

showImage(G0)

dt = 0.1

u1 = np.copy(u0)

for x in range(0, image.shape[1]):
    for y in range(0, image.shape[0]):
        u1[y][x] += dt*((get_u(G0,x+1,y)+get_u(G0,x,y))/2*(get_u(u0,x+1,y)-get_u(u0,x,y))
                -(get_u(G0,x,y)+get_u(G0,x-1,y)/2*(get_u(u0,x,y)-get_u(u0,x-1,y)))
                +(get_u(G0,x,y+1)+get_u(G0,x,y))/2*(get_u(u0,x,y+1)-get_u(u0,x,y))
                -((get_u(G0,x,y)+get_u(G0,x,y-1))/2*(get_u(u0,x,y)-get_u(u0,x,y-1))))

showImage(u1)

#Restore surrounding pixels?
for x in range(0, image.shape[1]):
    for y in range(0, image.shape[0]):
        if mask[y][x] > 128:
            u1[y][x] = image[y][x]

showImage(u1)
'''

def iteration(un, dt):
    G = g_matrix(un)

    unext = np.copy(u0)

    for x in range(0, image.shape[1]):
        for y in range(0, image.shape[0]):
            unext[y][x] += dt*((get_u(G,x+1,y)+get_u(G,x,y))/2*(get_u(un,x+1,y)-get_u(un,x,y))
                    -(get_u(G,x,y)+get_u(G,x-1,y)/2*(get_u(un,x,y)-get_u(un,x-1,y)))
                    +(get_u(G,x,y+1)+get_u(G,x,y))/2*(get_u(un,x,y+1)-get_u(un,x,y))
                    -((get_u(G,x,y)+get_u(G,x,y-1))/2*(get_u(un,x,y)-get_u(un,x,y-1))))
            unext[y][x] = np.clip(unext[y][x],0,255)
    
    #Restore surrounding pixels?
    '''
    for x in range(0, image.shape[1]):
        for y in range(0, image.shape[0]):
            if mask[y][x] > 128:
                unext[y][x] = image[y][x]
    '''    
    return unext
u = u0

showImage(u)

#ten seconds with N steps
N = 20

for k in range(0,N):
    #if k % 20 == 0:
        #showImage(u)

    u = iteration(u,0.25)
showImage(u)
#Restore surrounding pixels?
for x in range(0, image.shape[1]):
    for y in range(0, image.shape[0]):
        if mask[y][x] > 128:
            u[y][x] = image[y][x]
showImage(u)
