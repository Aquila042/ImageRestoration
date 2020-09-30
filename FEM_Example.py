import numpy as np
from utils import loadImage, saveImage, showImage, discrepancyScore, makeMask
from FEM import FEMLaplace

image = loadImage("pictures/128/005.jpeg", greyscale=False)

mask = loadImage("masks/128/circles.png")

originalimage = np.copy(image)

#Separate color channels and inpaint them
restoredimageR = FEMLaplace(image[:,:,0], mask)
restoredimageG = FEMLaplace(image[:,:,1], mask)
restoredimageB = FEMLaplace(image[:,:,2], mask)

#Combine color channels
restoredimage = np.dstack([restoredimageR,restoredimageG,restoredimageB])

showImage(np.concatenate([originalimage,np.dstack([mask,mask,mask]).astype(np.uint8),restoredimage],axis=1))

DSMask = makeMask("masks/128/circles.png") #Need the mask site index list
scoreR = discrepancyScore(originalimage[:,:,0], restoredimageR, DSMask[1])
scoreG = discrepancyScore(originalimage[:,:,1], restoredimageG, DSMask[1])
scoreB = discrepancyScore(originalimage[:,:,2], restoredimageB, DSMask[1])

scoreTot = (scoreR + scoreG + scoreB)/3
print("Average discrepancy score = " + str(scoreTot))


