from PIL import Image
import numpy as np

def loadImage(filename, greyscale = True):
    im = Image.open(filename)

    print("Loading " + filename)
    print(im.format, im.size, im.mode)

    if greyscale:
        #Greyscale conversion
        arr = np.array(im)

        grey = np.zeros((arr.shape[0],arr.shape[1]))

        for i in range(0,len(arr)):
            for k in range(0,len(arr[i])):
                color = int(0.3*arr[i][k][0] + 0.56*arr[i][k][1] + 0.11*arr[i][k][2])
                grey[i][k] = color
        
        return grey
    else:
        return np.array(im)

def showImage(array):
    if len(array.shape)==2:
        array3d = np.zeros((array.shape[0],array.shape[1],3))

        for i in range(0,len(array)):
            for k in range(0,len(array[i])):
                array3d[i][k] = array[i][k]

        newImg = Image.fromarray(array3d.astype(np.uint8))
        newImg.show()
    elif len(array.shape)==3:
        newImg = Image.fromarray(array)
        newImg.show()
    else:
        raise ValueError("Invalid array dimensions in showImage")

def saveImage(array, filename):
    if len(array.shape)==2:
        array3d = np.zeros((array.shape[0],array.shape[1],3))

        for i in range(0,len(array)):
            for k in range(0,len(array[i])):
                array3d[i][k] = array[i][k]

        newImg = Image.fromarray(array3d.astype(np.uint8))
        newImg.save(filename)
    elif len(array.shape)==3:
        newImg = Image.fromarray(array)
        newImg.save(filename)
    else:
        raise ValueError("Invalid array dimensions in saveImage")

def makeMask(imagePath):
    """
    Takes a black and white image (grey scale tecnicaly works)
    and return a strictly black and white mask and a list of
    site index for all maked pixels.
    """
    image = loadImage(imagePath)
    maskIndex = []#Saves the siteIndex of the mask
    
    for n in range(len(image)):
        for m in range(len(image[0])):
            if image[n][m] < 10:
                image[n][m] = 0
                maskIndex.append(n*len(image[n]) + m)
            else:
                image[n][m] = 255	
    return(image, maskIndex)
    

def IndexFlip(indexIn, rowLen):
    """
    Converts between site and pixel coordinate index
    site index must be a integer
    """
    if type(indexIn) == int or type(indexIn) == np.float64:
        cordX = int(indexIn % rowLen)
        cordY = int((indexIn - cordX)/rowLen)
        return (cordX, cordY)
    elif len(indexIn) == 2:
        return int(indexIn[1]*rowLen + indexIn[0])
    else:
        raise ValueError("index is of wrong type")
#int((intSites[intIndex] + x) % len(image[0]))
        

def discrepancyScore(imageIn, restoredIn, ActiveSites):
    """
    imageIn needs to be the original unmasked image.
    ActiveSites is the site index list given by makeMask
    """
    image = np.copy(imageIn).astype(np.float64)
    restored = np.copy(restoredIn).astype(np.float64)#preventing overflows
    
    missingOrig = []
    restoredValues = []
    for site in ActiveSites:
        cord = IndexFlip(site, len(image[0]))
        missingOrig.append(image[cord[1]][cord[0]])
        restoredValues.append(restored[cord[1]][cord[0]])
    n = len(ActiveSites)
    meanI = sum(missingOrig)/n
    sigma2 = 1/(n - 1)*sum([(I - meanI)**2 for I in restoredValues])
    chi2 = 0
    for n in range(len(restoredValues)):
        chi2 =+ (restoredValues[n] - missingOrig[n])**2
    chi2 = 1/n * chi2/sigma2
    return chi2
        
#create list of interior point neigbours [[[intPointIndex],[DB values]],...]
def findNeighbours(image, intSites):
    """ 
    takes image as array and a list of the site index for each interior point
    
    Returns a list where each entry contains the information of each neigbour to the coresponding site in intSites
    neigbours are seperated into two lists, interior and boudary
    the indecies for the relevant interior point in intSites is saved in the first list
    the values for the relevant boundary points are saved in the second list
    
    return = [[[site index 1, site index 2],[boundary value 1, boundary value 2]], ...]
    """
    neighbours = []
    for intIndex in range(len(intSites)):#for each interior point
        neighbours.append([[],[]])
        for x in [1 ,-1, len(image), -len(image)]:    #right, left, botom and top neigbours in site notation
            if (intSites[intIndex] + x) in intSites:   #check if neigbour is interor or a boundary
                neighbours[-1][0].append(intSites.index(intSites[intIndex]+x))
            else:
                cordx = int((intSites[intIndex] + x) % len(image[0]))
                cordy = int((intSites[intIndex] + x - cordx)/len(image[0]))
                neighbours[-1][1].append(image[cordy][cordx])
    return(neighbours)        
