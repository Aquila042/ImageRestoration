import utils as utl

testMask = utl.makeMask("pictures/128/smile.jpg")

#create list of interior point neigbours [[[intPointIndex],[DB values]],...]

def findNeigbours(image, intSites):
    """
    takes image as array and a list of the site index for each interior point
    
    Returns a list where each entry contains the information of each neigbour to the coresponding site in intSites
    neigbours are seperated into two lists, interior and boudary
    the indecies for the relevant interior point in intSites is saved in the first list
    the values for the relevant boundary points are saved in the second list
    
    return = [[[site index 1, site index 2],[boundary value 1, boundary value 2]], ...]
    """
    neigbours = []
    for intIndex in range(len(intSites)):#for each interior point
        neigbours.append([[],[]])
        for x in [1 ,-1, len(image), -len(image)]:    #right, left, botom and top neigbours in site notation
            if (intSites[intIndex] + x) in intSites:   #check if neigbour is interor or a boundary
                neigbours[-1][0].append(intIndex + x)
            else:
                cordx = int((intSites[intIndex] + x) % len(image[0]))
                cordy = int((intSites[intIndex] + x - cordx)/len(image[0]))
                neigbours[-1][1].append(image[cordy][cordx])
    return(neigbours)



testImage = utl.loadImage("pictures/128/001.jpeg")

testN = findNeigbours(testImage, testMask[1])

print(testN)