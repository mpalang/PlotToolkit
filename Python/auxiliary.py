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
    
    if zrange[0]>zrange[1]:
        zrange = (zrange[1],zrange[0])
        print('Make sure first zrange value is lower than second. Numbers were swapped.')
    
    if name=='fancy':
        levels = np.linspace(zrange[0],zrange[1],n_levels)
        if zrange[0]<0 and zrange[1]>0:
            zero=np.argmax(levels>0)
            cmap_neg=[get_cmap('Blues')(n/zero) for n in range(zero)]
            cmap_pos=[get_cmap('Reds')(n/(n_levels-zero)) for n in range(n_levels-zero)]
            cmap=cmap_neg[::-1]+ cmap_pos
            if not levels[zero-1] == 0:
                levels = np.insert(levels,zero,0)
                cmap.insert(zero,(1,1,1))
            
        elif zrange[0]<0:
            cmap=[get_cmap('Blues')(n/n_levels) for n in range(n_levels)]
        elif zrange[0]>0:
            cmap=[get_cmap('Reds')(n/n_levels) for n in range(n_levels)]
        
    else:
        levels=n_levels
        levels = np.linspace(zrange[0],zrange[1],levels+1)
        cmap=name
        
    return cmap,levels