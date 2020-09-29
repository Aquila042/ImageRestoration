import utils as utl
from mask import findNeighbours


testMask = utl.makeMask("masks/128/smile.jpeg")

testImage = utl.loadImage("pictures/128/001.jpeg")

testN = findNeighbours(testImage, testMask[1])
from SOR import SOR
testR = SOR(testMask[1],testN,15,1.9)#the two ones are the number of iterations and the relaxation constant.
#print(len(testR))
#print(testN)
#print(len(testMask[1]))
#print(len(testN))
print(testR)
