import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
from pathlib import Path
from auxiliary import make_cmap
import json
with open('rcParams.json','r') as f:
    Params = json.load(f)
    

# =============================================================================
# Standard Contourplot
# =============================================================================

def contour(x,
             y,
             Z,
             xrange=None,
             yrange=None,
             zrange=None,
             separate=True,
             title=None,
             xlabel=None,
             ylabel=None,
             dpi=100,
             cmap=None,
             **rcParams
             ):
    """

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    y : TYPE
        DESCRIPTION.
    Z : TYPE
        DESCRIPTION.
    xmin : TYPE, optional
        DESCRIPTION. The default is None.
    xmax : TYPE, optional
        DESCRIPTION. The default is None.
    ymin : TYPE, optional
        DESCRIPTION. The default is None.
    ymax : TYPE, optional
        DESCRIPTION. The default is None.
    zmin : TYPE, optional
        DESCRIPTION. The default is None.
    zmax : TYPE, optional
        DESCRIPTION. The default is None.
    separate : TYPE, optional
        DESCRIPTION. The default is True.
    title : TYPE, optional
        DESCRIPTION. The default is None.
    xlabel : TYPE, optional
        DESCRIPTION. The default is None.
    ylabel : TYPE, optional
        DESCRIPTION. The default is None.
    dpi : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    fig

    """

    if Path('rcParams.json').exists():
        with open('rcParams.json','r') as f:
            Params = json.load(f)
        mpl.rcParams.update(**Params)
    
    # from warnings import filterwarnings
    # filterwarnings('ignore',"_nolegend_")
    
    if type(x).__module__ != np.__name__:
        x=np.arange(0,Z.shape[1],1)
        
    if type(y).__module__ != np.__name__:
        y=np.arange(0,Z.shape[0],1)
    
    if zrange:
        zrange=[zrange[0],zrange[1]]
        if zrange[0]==None:
            zrange[0]=np.nanmin(Z)-1e-6
        if zrange[1]==None:
            zrange[1]=np.nanmax(Z)-1e-6
    else:
        zrange=[np.nanmin(Z),np.nanmax(Z)]
       
    cmap_name = 'fancy'
    cmap,levels = make_cmap(name=cmap_name,zrange=zrange)
    
    fig=plt.figure(dpi=dpi,figsize=(16,12))
    # ax=set_size((16,12),fig)
    
    if cmap_name=='fancy':    
        img=plt.contourf(y,x,Z.T,levels=levels,colors=cmap,extend='both') #TODO: positive extend shows wrong color
    else:
        img=plt.contourf(y,x,Z.T,levels=levels,cmap=cmap,extend='both')
    
    plt.xlim(xrange)
    plt.ylim(yrange)
        
    plt.colorbar(img,anchor=(1,1))
    
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.tick_params(axis='x', direction='in')
    plt.tick_params(axis='y', direction='in')
    
    ax=plt.gca()
    ax.set_title(title)
    
    # mpl.rcParams.update(rcParams)
    
    plt.show() 
    
    return fig
        


# =============================================================================
# Timecontour
# =============================================================================


def timecontour(x,y,Z,
              x_range=[None,None],
              axis_break=1,
              y_range=[None,None],
              Z_range=[None,None],
              title=None,
              zero_contour=False,
              orientation='horizontal',
              dpi=200):
    
    if Path('rcParams.json').exists():
        with open('rcParams.json','r') as f:
            Params = json.load(f)
        mpl.rcParams.update(**Params)
    
    mpl.rcParams.update({'figure.figsize': (16,4*16/6),
                         'lines.linewidth': 4,
                        'lines.markersize': 8,
                        'font.size': 50,
                        'axes.linewidth': 3,
                        # 'legend.fontsize':15,
    #                     'axes.titlesize': fontsize-10,
    #                     'axes.titlepad': 20, 
                        'axes.labelpad': 3,
                        
                        'xtick.major.size': 10, 'xtick.major.width': 2, # 'xtick.major.pad': 10,
                        'xtick.minor.size': 5, 'xtick.minor.width': 2, 
                        'ytick.major.size': 10, 'ytick.major.width': 2, # 'ytick.major.pad': 10
                        'ytick.minor.size': 5, 'ytick.minor.width': 2,
                        
                        })
        
    if x_range[0]==None:
        x_range[0]=np.nanmin(x)-1e-6
    if x_range[1]==None:
        x_range[1]=np.nanmax(x)-1e-6
        
    if y_range[0]==None:
        y_range[0]=np.nanmin(y)-1e-6
    if y_range[1]==None:
        y_range[1]=np.nanmax(y)-1e-6
        
    if Z_range[0]==None:
        Z_range[0]=np.nanmin(Z)-1e-6
    if Z_range[1]==None:
        Z_range[1]=np.nanmax(Z)-1e-6
    
    
    if orientation=='horizontal':    
        fig,ax=plt.subplots(1,2,gridspec_kw={'width_ratios':[1,2],'wspace':0.012},dpi=dpi)
    else:
        fig,ax=plt.subplots(2,1,gridspec_kw={'height_ratios':[2,1],'hspace':0.02},dpi=dpi)
   
    ##############
    ####Contour
    cmap,levels = make_cmap()
    
    ix1 = np.argmax(x>x_range[0])
    ix2 = np.argmax(x>axis_break)
    ix3 = np.argmax(x>x_range[1])
    
    if orientation=='horizontal':   
        ax[0].contourf(x[ix1:ix2],y,Z[:,ix1:ix2],
                          levels=levels,colors=cmap,extend='both',
                          vmin=Z_range[0],vmax=Z_range[1],
                         )
    
        img=ax[1].contourf(x[ix2:ix3],y,Z[:,ix2:ix3],
                          levels=levels,colors=cmap,extend='both',
                          vmin=Z_range[0],vmax=Z_range[1],
                         )

        ax[1].set_xscale('log')
        ax[1].set_yticks([])
  
        ax[1].text(0.1, -0.15, 'wl/nm', va='center',transform=ax[1].transAxes)
        fig.colorbar(img,ax=ax[0])
        ax[0].set_ylabel('$\Delta$t/ps')
        ax[0].set_title=title
        
    else:   
        ax[1].contourf(x,y[np.argmax(y>y_range[0]):np.argmax(y>axis_break)],
                       Z[np.argmax(y>y_range[0]):np.argmax(y>axis_break),:],
                       levels=levels,colors=cmap,extend='both',
                       vmin=Z_range[0],vmax=Z_range[1],
                      )
    

    
        img=ax[0].contourf(x,
                           y[np.argmax(y>axis_break):np.argmax(y>y_range[1])],
                           Z[np.argmax(y>axis_break):np.argmax(y>y_range[1]),:],
                           levels=levels,colors=cmap,extend='both',
                           vmin=Z_range[0],vmax=Z_range[1],
                          )

        
        if zero_contour:
            contour1 = ax[0].contour(x, y[np.argmax(y>axis_break):np.argmax(y>y_range[1])], 
                                     Z[np.argmax(y>axis_break):np.argmax(y>y_range[1]),:], 
                                     levels=[0], colors='black', linestyles=':',linewidths=1)
            contour2 = ax[1].contour(x, y[np.argmax(y>y_range[0]):np.argmax(y>axis_break)], 
                                    Z[np.argmax(y>y_range[0]):np.argmax(y>axis_break),:], 
                                    levels=[0], colors='black', linestyles=':',linewidths=1)
        
        ax[0].set_yscale('log')
        ax[0].set_xticks([])
  
        
        ax[0].text(-0.2, 0.2, '$\Delta$t', va='center',transform=ax[0].transAxes,rotation='vertical')
        ax[1].set_xlabel('wl/nm')
        fig.colorbar(img,ax=ax)
        
        ax[0].set_title(title)
    
     
    
    
    plt.show()
    
    return fig