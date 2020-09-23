import utils as utl

testMask = utl.makeMask("pictures/128/001.jpeg")

#create list of interior point neigbours [[[intPointIndex],[DB values]],...]
#UNFINISHED
def findNeigbours(image, intSites):#takes image and mask as arrays
	neigbours = []
	for intIndex in range(len(intSites)):
		neigbours.append([[],[]])
		for x in [1 ,-1, len(image), -len(image)]:
			if intSites[intIndex] + x in intSites == True:
				neigbours[-1][0].append(intIndex)
			else:
				cordx = int(intSites[intIndex] % len(image[0]))
				cordy = int((intSites[intIndex] - cordx)/len(image[0]))
				neigbours[-1][1].append(image[cordy][cordx])
	return(neigbours)

testImage = utl.loadImage("pictures/128/001.jpeg")
