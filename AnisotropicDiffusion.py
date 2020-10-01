from utils import loadImage, showImage
from FEM import FEMLaplace
import numpy as np

#Diffusivity constant
#K = 1

#Diffusivity function
def g(norm_laplacian_squared,K):
    return 2*np.exp(-norm_laplacian_squared/(K**2))

#def g(x):
#    return 1/(1+x/(K**2))**2

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
def g_matrix(u, K):
    G = np.zeros(u.shape)
    for x in range(0,u.shape[1]):
        for y in range(0,u.shape[0]):
            norm_laplacian_squared = max((get_u(u,x+1,y)-get_u(u,x,y))*(get_u(u,x,y)-get_u(u,x-1,y)),0) 
            + max((get_u(u,x,y+1)-get_u(u,x,y))*(get_u(u,x,y)-get_u(u,x,y-1)),0) 
            #norm_laplacian_squared = ((get_u(u,x+1,y)-get_u(u,x-1,y))/2)**2+((get_u(u,x,y+1)-get_u(u,x,y-1))/2)**2
            G[x][y] = g(norm_laplacian_squared, K)
    
    return G

def iteration(un, _mask,dt, K, _image):
    G = g_matrix(un, K)

    unext = np.copy(un)

    for x in range(0, _image.shape[1]):
        for y in range(0, _image.shape[0]):
            unext[y][x] += dt*((get_u(G,x+1,y)+get_u(G,x,y))/2*(get_u(un,x+1,y)-get_u(un,x,y))
                    -(get_u(G,x,y)+get_u(G,x-1,y)/2*(get_u(un,x,y)-get_u(un,x-1,y)))
                    +(get_u(G,x,y+1)+get_u(G,x,y))/2*(get_u(un,x,y+1)-get_u(un,x,y))
                    -((get_u(G,x,y)+get_u(G,x,y-1))/2*(get_u(un,x,y)-get_u(un,x,y-1))))
            unext[y][x] = np.clip(unext[y][x],0,255)
    
    #Restore surrounding pixels?
    for x in range(0, _image.shape[1]):
        for y in range(0, _image.shape[0]):
            if _mask[y][x] > 128:
                unext[y][x] = _image[y][x]
    
    return unext

def anisotropicDiffusion(_image, _mask, N, K):

    u0 = np.zeros((_image.shape[0],_image.shape[1]))

    #Use the Laplace inpainted image as an initial guess
    laplacerestored = np.copy(FEMLaplace(_image, _mask))
    
    for x in range(0,_image.shape[1]):
            for y in range(0,_image.shape[0]):
                if _mask[y][x] < 128:
                    u0[y][x] = laplacerestored[y][x] 
                else:
                    u0[y][x] = _image[y][x]

    u = u0

    #showImage(u)

    for k in range(0,N):
        u = iteration(u, _mask, 0.01, K, _image)

    #showImage(u)

    #Restore surrounding pixels
    for x in range(0, _image.shape[1]):
        for y in range(0, _image.shape[0]):
            if _mask[y][x] > 128:
                u[y][x] = _image[y][x]

    #showImage(u)

    return u

'''
image = loadImage("pictures/256/003.jpeg").astype(np.float64)
mask = loadImage("masks/256/circles.png").astype(np.float64)

anisotropicDiffusion(image, mask, 10, 1)
'''
