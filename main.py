import utils as utl
from mask import findNeighbours

testMask = utl.makeMask("masks/128/smile.jpeg")

testImage = utl.loadImage("pictures/128/001.jpeg")

testN = findNeighbours(testImage, testMask[1])

print(testN)
