# -*- coding: utf-8 -*-
"""
This is a function to make nice figures with minimum effort.
"""
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as mticker
from matplotlib.cm import ScalarMappable
import matplotlib.gridspec as gridspec
from auxiliary import set_size

try:
    from matplotlib import colormaps
except ImportError as e:
    from matplotlib import cm as colormaps
    print('importing cm instead of colormaps')
from matplotlib import pyplot as plt

from pathlib import Path
import sys
import json
with open('rcParams.json','r') as f:
    Params = json.load(f)

#%%





def plot( x,Y,
            label=[],label_box=False,anchor=None,
            title=None,
            xlabel=None, ylabel=None,
            ROI=None, xrange=(None,None), yrange=(None,None),
            linestyles=None,
            fill=None,fill_label='_nolegend_',
            colors=None,cmap='autumn',
            padx=0.04,pady=0.1,
            xrule=True,
            vline=[],
            xline=None,
            xscale='linear',
            yscale='linear',
            gui=False,
            
            figsize=(16,9),
            dpi=200,
            rcParams={}
            ):
    
    """
    Input:
        x: x-values for x-axis
        Y: list of y-values. If x-values differ from 'x', data has to be inserted as touple (x2,y2).
        label: List of curve-labels.
        label_box: options: True, False, 'outside'
        title: title of plot,
        xlabel: x-axis label.
        ylabel: y-axis label.
        ROI: range of data to plot,
        xrange: x-range for plotting as touple (left,right).
        yrange: y-range for plotting as touple (lower,upper)
        linestyles: list with linestyles 'o' for scatter plot. Length has to be same as Y.
        fill: touple of three elements: (x-values,y-values,scaling-factor),
        fill_label: label for fill curve.
        colors: list with colors. Length has to be same as Y.
        padx: white space around data in x-direction.
        pady: white space around data in y-direction.
        xrule: horizontal line at y=0.
        vline: draws vertical line at positions [x1,x2,...]
        xscale: x-scale. options: 'linear', 'log', 'symlog'
        gui: Graphical user interface.
        dpi: resolution for figures. ~200 for quick view, ~2000 for final images.
        
    Output:
        figure instance from pyplot
        if save option is True, plots are saved in Figure folder in base path.
    
    """
    # mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams.update(**Params)
    mpl.rcParams.update(**rcParams)
    
    colors_list=['#515151', '#F14040', '#1A6FDF', '#37AD6B', '#B177DE', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#d62728','#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    try:
        colors_grad=colormaps[cmap]
    except:
        colors_grad=colormaps.get_cmap(cmap)
    
    from warnings import filterwarnings
    filterwarnings('ignore')
    
    if gui:
        mpl.use('TkAgg')
        import matplotlib.pyplot as plt
    else:
        
        import matplotlib.pyplot as plt
    
    ##########################################
    # this function wants to deal with lists #  
    ##########################################
    
    if type(Y)!=list:
        Y=[Y]
    
    if linestyles==None or len(linestyles)!=len(Y):
        linestyles=[None]*len(Y)
        

    if colors=='grad':
        colors=colors_grad(np.linspace(0,1,len(Y)))
    elif colors==None or len(colors)!=len(Y):
        colors=colors_list[:len(Y)]
    
    ###########################################
    # if no x-values are provided, make some: #
    ###########################################
    
    
     
    ################################
    #Cut Data accordingly and plot #
    ################################

    fig=plt.figure(dpi=dpi)
    ax=set_size(figsize,fig)
    
    mpl.rcParams.update(**rcParams)
    for n,y in enumerate(Y):
        if type(y)==tuple: #if you have data with different x-scales, you need to specify the dataset as (x,y) touple.
            if type(y[0]).__module__ != np.__name__:
                    x=np.arange(0,y[1].shape[0],1)             
            else:
                x=y[0]
            
            if ROI:
                fromx=np.argmax(x>ROI[0])
                tox=np.argmax(x>ROI[1])
                if tox==0:
                    tox=len(x)  
                x0=x[fromx:tox]
                y0=y[1][fromx:tox]
            else:
                x0=x
                y0=y[1]

                
        else:
            if type(x).__module__ != np.__name__:
                    x=np.arange(0,y.shape[0],1)
                    print('Attention: x input not a numpy array! Integer x-values are created.')
            if ROI:
                fromx=np.argmax(x>ROI[0])
                tox=np.argmax(x>ROI[1])
                if tox==0:
                    tox=len(x)   
                x0=x[fromx:tox]
                y0=y[fromx:tox]
            else:
                x0=x
                y0=y
            
        if linestyles[n]=='o' or linestyles[n]=='+':
            plt.plot(x0,y0,linestyles[n],markersize=15,markeredgewidth=4,markerfacecolor='white',color=colors[n])
        else:
            plt.plot(x0,y0,linestyle=linestyles[n],color=colors[n])
    
    
    if fill:
        fromx=np.argmax(fill[0]>np.min(x0))
        tox=np.argmax(fill[0]>np.max(x0))-1
        if tox==0:
            tox=len(fill[0])
        
        plt.fill_between(fill[0][fromx:tox],fill[1][fromx:tox]*fill[2],color="#01153E",alpha=0.2)
        # if xrule:
        #     label.append('_nolegend_')
        label.append(fill_label)
    
    ################
    #Layout stuff: #
    ################
    
    # ax=plt.gca()
    if yrange:
        ax.set_ylim(bottom=yrange[0])
        ax.set_ylim(top=yrange[1])
    if xrange:
        if xrange[0]:
            ax.set_xlim(left=xrange[0])
        if xrange[1]:
            ax.set_xlim(right=xrange[1])
    
    ax.margins(padx,pady)
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)

    if xrule:
        plt.axhline(y=0, color='k', linewidth=2)   
        label.append('_nolegend_')
        
    if vline:
        for i in vline:
            plt.axvline(x=i,linestyle='--')
        
    plt.title=title#,wrap=True) #TODO: Title gets cut off if multiple lines.
    ax.set_title(title)
    
    if len(label)==0:
         for n in range(len(Y)):
             label.append('Curve'+str(n+1))
    
    loc=None
    if anchor:
        loc='upper left'
        if type(anchor)==str:
            loc=anchor
            anchor=None
    
        
    if label_box=='outside':
        plt.legend(label,frameon=True,bbox_to_anchor=(1,1))
    else:
        if label_box:
            plt.legend(label,frameon=True,bbox_to_anchor=anchor,loc=loc)
        else:
            plt.legend(label,frameon=False,bbox_to_anchor=anchor,loc=loc)
    
    
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    
    plt.minorticks_on()    
        
    return fig
    
        




def timeplot( x,
            Y,
            
            label=[],label_box=False,anchor=None,#label_frame=False,label_anchor=None,
            xlabel_style='scientific',
            
            title=None,
            xlabel="$\Delta$t / ps",
            ylabel="$\Delta$mOD",
            labelpad=(0.05,0.05),
            
            xrange=None,
            yrange=None,
            
            linestyles=None,
            colors=None,cmap='autumn',
            
            padx=0.04,
            pady=0.2,
            
            xrule=True,
            xline=None,
            x_break=2,
            

            gui=False,
            figsize=(16,9),
            dpi=200,
            rcParams=None,
            ):
    
    """
    Input:
        x: x-values for x-axis
        Y: list of y-values. If x-values differ from 'x', data has to be inserted as touple (x2,y2).
        label: List of curve-labels.
        title: title of plot,
        xlabel: x-axis label.
        ylabel: y-axis label.
        labelpad: padding between label and ticklabel
        xrange: x-range for plotting as touple (left,right).
        yrange: y-range for plotting as touple (lower,upper)
        linestyles: list with linestyles 'o' for scatter plot. Length has to be same as Y.
        colors: list with colors. Length has to be same as Y.
        padx: white space around data in x-direction.
        pady: white space around data in y-direction.
        xrule: horizontal line at y=0.
        xline: plot vertical line at x='xline'
        x_break: has to be specified for 'symlog'. Determines where to switch from linear to log.
        gui: Graphical user interface.
        dpi: resolution for figures. ~200 for quick view, ~2000 for final images.
        
    Output:
        figure instance from pyplot
        if save option is True, plots are saved in Figure folder in base path.
    
    """
    
    from warnings import filterwarnings
    filterwarnings('ignore',"_nolegend_")
    
    mpl.rcParams.update(**Params)

    
    colors_list=['#515151', '#F14040', '#1A6FDF', '#37AD6B', '#B177DE', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#d62728',
                 '#515151', '#F14040', '#1A6FDF', '#37AD6B', '#B177DE', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#d62728']
    
    try:
        colors_grad=colormaps[cmap](np.arange(0.001,0.999,1/(len(Y)-0.9)))
    except:
        colors_grad=mpl.cm.get_cmap(cmap)
    
    if gui:
        mpl.use('TkAgg')
        import matplotlib.pyplot as plt
    else:        
        import matplotlib.pyplot as plt
            
    ##########################################    
    # this function wants to deal with lists # 
    ##########################################
    
    if type(Y)!=list:
        Y=[Y]
    
    if linestyles==None or len(linestyles)!=len(Y):
        linestyles=[None]*len(Y)
    
    if colors=='grad':
        colors=[colors_grad(i) for i in range(0,1000,int(1000/len(Y)))]
    elif colors==None or len(colors)!=len(Y):
        colors=colors_list[:len(Y)]
    

    ############
    #plot data #
    ############
    if rcParams:
        mpl.rcParams.update(**rcParams)

    fig=plt.figure(dpi=dpi,figsize=figsize)
    
    gs = gridspec.GridSpec(1, 2,width_ratios=[2,3],wspace=0.02)
     
    ax=plt.subplot(gs[0])
    ax2=plt.subplot(gs[1])
 


    ax2.set_xscale('log')

    for n,y in enumerate(Y):
        if type(y)==tuple: #if you have data with different x-scales, you need to specify the dataset as (x,y) touple.
            
            if type(y[0]).__module__ != np.__name__:
                x0=np.arange(0,y[1].shape[0],1)
            else:
                if xrange:
                    if xrange[0]:
                        fromx=np.argmax(y[0]>xrange[0])
                    else:
                        fromx=0
                    if xrange[1]:
                        tox=np.argmax(y[0]>xrange[1])
                    else:
                        tox=len(y[0])-1               
                    if tox==0:
                        tox=len(y[0])-1   
                        
                        
                    x0=y[0][fromx:tox]
                    y0=y[1][fromx:tox]
                    
                    ax.set_xlim(y[0][fromx]-0.2,x_break-0.001)
                    ax2.set_xlim(x_break+0.001,y[0][tox]*1.2)
                else:
                    x0=y[0]
                    y0=y[1]
        else:
            # if no x-values are provided, make some: 
            if type(x).__module__ != np.__name__:
                x0=np.arange(0,y.shape[0],1)
            else:
                if xrange:
                    if xrange[0]:
                        fromx=np.argmax(x>xrange[0])
                    else:
                        fromx=0
                    if xrange[1]:
                        tox=np.argmax(x>xrange[1])
                    else:
                        tox=len(x)-1               
                    if tox==0:
                        tox=len(x)-1   
                    x0=x[fromx:tox]
                    y0=y[fromx:tox]
                    
                    ax.set_xlim(x[fromx]-0.2,x_break-0.001)
                    ax2.set_xlim(x_break+0.001,x[tox]*1.2)
                else:
                    x0=x
                    y0=y
        if linestyles[n]=='o':
            ax.scatter(x0,y0,s=150,facecolors='none',edgecolors=colors[n],linewidth=2)
            ax2.scatter(x0,y0,s=150,facecolors='none',edgecolors=colors[n],linewidth=2)
        else:
            ax.plot(x0,y0,linestyle=linestyles[n],color=colors[n])
            ax2.plot(x0,y0,linestyle=linestyles[n],color=colors[n])

    ################
    #Layout stuff: #
    ################
    
    ax.set_xlim(np.min(x0)-0.2,x_break-0.001)
    ax2.set_xlim(x_break+0.001,np.max(x0)*1.2)
    
    if yrange:
        
        ax.set_ylim(bottom=yrange[0])
        ax.set_ylim(top=yrange[1])
        ax.margins(padx,pady)
    
        ax2.set_ylim(bottom=yrange[0])
        ax2.set_ylim(top=yrange[1])
        ax2.margins(padx,pady)
        
    # else:
        
    #     ax.set_ylim(bottom=yrange[0])
    #     ax.set_ylim(top=yrange[1])
    #     ax.margins(padx,pady)
    
    #     ax2.set_ylim(bottom=yrange[0])
    #     ax2.set_ylim(top=yrange[1])
    #     ax2.margins(padx,pady)
    
    #############################
    #And some layout adjustment:#
    #############################
    
    if xrule:
        ax.axhline(y=0, color='k', linewidth=2)  
        ax2.axhline(y=0, color='k', linewidth=2) 
        label.append('_nolegend_')

    ax.set_title(title, loc='left')
    
    if len(label)==0:
         for n in range(len(Y)):
             label.append('Curve'+str(n+1))
    
    loc=None
    if anchor:
        loc='upper left'
        if type(anchor)==str:
            loc=anchor
            anchor=None
    if label_box=='outside':
        plt.legend(label,frameon=True,bbox_to_anchor=(1,1))
    else:
        if label_box:
            plt.legend(label,frameon=True,bbox_to_anchor=anchor,loc=loc)
        else:
            plt.legend(label,frameon=False,bbox_to_anchor=anchor,loc=loc)
    # plt.legend(label,frameon=label_frame,bbox_to_anchor=label_anchor)
    
    # hide the spines between ax and ax2
    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    
    ######################
    ##little break lines #
    ##################################################################################
                                                                                     #
    d = .015  # how big to make the diagonal lines in axes coordinates               #
    # arguments to pass to plot, just so we don't keep repeating them                #
    kwargs = dict(transform=ax.transAxes, color='k', linewidth=2, clip_on=False)     #
    ax.plot((1-d, 1+d), (-d, +d), **kwargs)        # top-left diagonal               #
    ax.plot((1- d, 1 + d), (1-d, 1+d), **kwargs)  # top-right diagonal               #
                                                                                     #
    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes              #
    ax2.plot((-2/3*d, +2/3*d), (- d, + d), **kwargs)  # bottom-left diagonal         #
    ax2.plot((- 2/3*d, + 2/3*d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal  #
    ##################################################################################    
    
    ax.minorticks_on()    
    ax2.minorticks_on()    

    #no scientific notation
    if xlabel_style=='plain':
        ax2.xaxis.set_minor_formatter(mticker.ScalarFormatter())
        ax2.xaxis.set_major_formatter(mticker.ScalarFormatter())
        ax2.ticklabel_format(style=xlabel_style,axis='x')

    ax.tick_params(labelright=False)
    ax2.tick_params(labelleft=False,which='major',left=False,right=True)
    ax2.tick_params(which='minor',left=False)
    
    if xline:
        ax.axvline(x=xline,linestyle='...')
    
    ###
    #Axis label
    ###
    fig.text(0.5, 0-labelpad[0], xlabel, ha='center')
    fig.text(0-labelpad[1], 0.5, ylabel, va='center', rotation='vertical')
    ####
    
    plt.tight_layout()
        
    return fig



# =============================================================================
# %% Fit Plots:
# =============================================================================

def SF_Plot_Results(x,y,y_fit,residuum,figsize=(16,9)):
            
    fig,ax=plt.subplots(nrows=2,height_ratios=(2,1),dpi=40,figsize=(16,9))
    ax[0].axhline(y=0,color='black',linewidth=1)
    ax[0].plot(x,y,'o')
    ax[0].plot(x,y_fit)
    ax[0].set_xscale('log')
    ax[0].set_xticks([])
    
    ax[1].plot(x,residuum,'o')
    ax[1].axhline(y=0,color='black',linewidth=1)
    ax[1].set_xscale('log')
    
    return fig,ax
    
def GF_Plot_Results(x,y,y_fit,residuum,figsize=(16,9)):
        
    fig=plt.figure(dpi=50)
    ax=set_size(figsize,fig)
    
    return fig,ax

     