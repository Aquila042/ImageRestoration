from AnisotropicDiffusion import anisotropicDiffusion
from utils import saveImage, loadImage, showImage, makeMask, discrepancyScore 
from FEM import FEMLaplace
import numpy as np

images = ["pictures/128/001.jpeg"]

for filename in images:
    print(filename)

    imageR = loadImage(filename, greyscale=False)[:,:,0]
    imageG = loadImage(filename, greyscale=False)[:,:,1]
    imageB = loadImage(filename, greyscale=False)[:,:,2]
    mask, activeSites = makeMask("masks/128/circles.png")

    restoredR = anisotropicDiffusion(imageR, mask, 10, 5)
    restoredG = anisotropicDiffusion(imageG, mask, 10, 5)
    restoredB = anisotropicDiffusion(imageB, mask, 10, 5)

    restored = np.dstack([restoredR,restoredG,restoredB]).astype(np.uint8)

    score = (discrepancyScore(imageR, restoredR, activeSites) + discrepancyScore(imageG, restoredG, activeSites) +discrepancyScore(imageB, restoredB, activeSites))/3

    print("Anisotropic diffusion discrepancy score: ", score)

    laplaceRestoredR = FEMLaplace(imageR, mask)
    laplaceRestoredG = FEMLaplace(imageG, mask)
    laplaceRestoredB = FEMLaplace(imageB, mask)

    laplacescore = (discrepancyScore(imageR, laplaceRestoredR, activeSites) + discrepancyScore(imageG, laplaceRestoredG, activeSites) +discrepancyScore(imageB, laplaceRestoredB, activeSites))/3

    print("Laplace eq. discrepancy score: ", laplacescore)

    laplacerestored = np.dstack([laplaceRestoredR,laplaceRestoredG,laplaceRestoredB]).astype(np.uint8)


    showImage(np.concatenate([np.dstack([imageR,imageG,imageB]),np.dstack([mask,mask,mask]),laplacerestored,restored], axis=1).astype(np.uint8))

    #saveImage(np.concatenate([np.dstack([imageR,imageG,imageB]),np.dstack([mask,mask,mask]),laplacerestored,restored], axis=1).astype(np.uint8), "001_comparisoni.jpeg")

