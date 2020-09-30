import utils as utl
import numpy as np


testMask = utl.makeMask("masks/128/circles.png")

testImage = utl.loadImage("pictures/128/005.jpeg")
image = np.copy(testImage)
testN = utl.findNeighbours(testImage, testMask[1])
from SOR import SOR, RestoreIndex
testR = SOR(testMask[1],testN,30,1.9)#the two ones are the number of iterations and the relaxation constant.
#print(len(testR))
#print(testN)
#print(len(testMask[1]))
#print(len(testN))
#print(testR)

FixedImg = np.copy(RestoreIndex(image, testR, testMask[1]))
utl.showImage(FixedImg)
utl.showImage(image)
DS = utl.discrepancyScore(image, FixedImg, testMask[1])
print(DS)


#%%
#Uppscale example
from PIL import Image, ImageOps

orgImage = utl.loadImage("pictures/128/002.jpeg")

upImage = Image.fromarray(orgImage.astype(np.uint8))
upImage = upImage.resize((252, 252))
upImagePad = ImageOps.expand(upImage, border=3, fill ="black")
upScaled = np.copy(np.array(upImagePad))

mesh = utl.makeMask("masks/256/upscaling_grid_pad.png")
mechN = utl.findNeighbours(upScaled, mesh[1])

smooth = SOR(mesh[1], mechN, 10, 1.9)
doubleSizeIm = np.copy(RestoreIndex(upScaled, smooth, mesh[1]))
utl.showImage(doubleSizeIm)