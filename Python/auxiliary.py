# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 18:22:24 2026

@author: morit
"""
# from matplotlib.cm import get_cmap
from matplotlib.pyplot import get_cmap
from mpl_toolkits.axes_grid1 import Divider, Size
import numpy as np

#%% Auxiliary


def set_size(figsize,fig):
        
    h=[Size.Fixed(0), Size.Fixed(figsize[0])]
    v=[Size.Fixed(0),Size.Fixed(figsize[1])]
    
    divider = Divider(fig, (0,0,1,1),h,v, aspect=False)
    
    ax = fig.add_axes(divider.get_position(),axes_locator=divider.new_locator(nx=1, ny=1))
    
    return ax   

# =============================================================================
# color stuff
# =============================================================================

def make_cmap(name='fancy',n_levels=40,zrange=(-1,1)):
    
    if name=='fancy':
        levels = np.linspace(zrange[0],zrange[1],n_levels)
        zero=np.argmax(levels>0)
        levels=np.concatenate((levels[:zero],[0],levels[zero:]))
        cmap_neg=[get_cmap('Blues')(n/zero) for n in range(n_levels-zero)]
        cmap_pos=[get_cmap('Reds')(n/(n_levels-zero)) for n in range(n_levels-zero)]
        cmap=cmap_neg[::-1]+[(1,1,1)]+ cmap_pos
    
    elif not name:
        levels=20
        levels = np.linspace(zrange[0],zrange[1],levels+1)
        cmap=get_cmap('rainbow')
    else:
        levels=20
        levels = np.linspace(zrange[0],zrange[1],levels+1)
        cmap=name
        
    return cmap,levels