import utils as utl
from mask import findNeighbours
import numpy as np


testMask = utl.makeMask("masks/128/circles.png")

testImage = utl.loadImage("pictures/128/005.jpeg")
Image = np.copy(testImage)
testN = findNeighbours(testImage, testMask[1])
from SOR import SOR, RestoreIndex
testR = SOR(testMask[1],testN,30,1.9)#the two ones are the number of iterations and the relaxation constant.
#print(len(testR))
#print(testN)
#print(len(testMask[1]))
#print(len(testN))
#print(testR)

FixedImg = np.copy(RestoreIndex(Image, testR, testMask[1]))
utl.showImage(FixedImg)
utl.showImage(Image)
DS = utl.discrepancyScore(Image, FixedImg, testMask[1])
print(DS)