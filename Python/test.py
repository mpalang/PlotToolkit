from pathlib import Path
import numpy as np
from plotting3D import contour,timecontour

x = np.genfromtxt(Path('TestData/t.txt'))
y = np.genfromtxt(Path('TestData/wl.txt'))
Z = np.genfromtxt(Path('TestData/Z.txt'))


timecontour(x,y,Z,axis_break=20,Z_range=(-0.005,0.005))