from pathlib import Path
import numpy as np
from plotting3D import contour,timecontour

t = np.genfromtxt(Path('TestData/t.txt'))
wl = np.genfromtxt(Path('TestData/wl.txt'))
Z = np.genfromtxt(Path('TestData/signal.txt'))

# t = np.genfromtxt(Path('TestData/x.txt'))
# wl = np.genfromtxt(Path('TestData/y.txt'))
# Z = np.genfromtxt(Path('TestData/z.txt'))


fig,ax = timecontour(wl,t,Z,
        zrange=(-0.012,0.012),
        # xrange=(420,720),
        # yrange=(-1,10),
        axis='vertical',axis_break=30,
        )