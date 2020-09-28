import utils as utl
from mask import findNeighbours

testMask = utl.makeMask("masks/128/3x3.png")

testImage = utl.loadImage("pictures/128/001.jpeg")

testN = findNeighbours(testImage, testMask[1])

print(testN)
