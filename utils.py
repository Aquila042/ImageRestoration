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

