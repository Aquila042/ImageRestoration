# ImageRestoration

Project for FytN03 module B.

Restore "graffitied" images with numerical PDEs.

Requirements:

Check requirements.txt

or let pip handle it:

pip install -r requirements.txt

--Basic version--
Grayscale image

Masks can be loaded as images with: white as saved pixels and black as masked pixels.

The Laplace equation is solved through both FDM and FEM, in SOR.py and FEM.py respectively

Discrepancy score to measure how good the method is.

Examples:

FDM\_example.py

--Anisotropic diffusion--

In AnisotropicDiffusion.py there is an example of solving the Laplace equation with FEM, followed by anisotropic diffusion. 
