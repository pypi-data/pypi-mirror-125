import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import glob, os
from matplotlib import cm


def feature_plot(h, rank, parameter_string, dst_folder,
                 shape=(15,30),
                 savefile=True,
                 showplot=False):
    from matplotlib.gridspec import GridSpec as gs
    if rank % 5 == 0:
        nrows = int(rank / 5)
    else:
        nrows = int(rank / 5) + 1
    ncols = 5
    fig = plt.figure(figsize=(2 * ncols, nrows*1.1+0.5))
    grids = gs(nrows*2+1, ncols, hspace=1)
    ax0 = fig.add_subplot(grids[0,:])
    ax0.text(0,0.5,parameter_string,ha='left',fontsize=12)
    ax0.axis('off')
    for i in range(rank):
        x = int(i / 5)
        y = i % 5
        ax = fig.add_subplot(grids[x*2+1:x*2+3, y])
        ax.imshow(h[i].reshape(shape), aspect='auto', cmap='viridis')
        ax.set_title('feature {}'.format(i + 1))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    if savefile:
        plt.savefig('{}{}_rank_{}.png'.format(dst_folder, parameter_string, rank),
                    bbox_inches='tight', dpi=160, transparent=True)
    if not showplot:
        plt.close()


def plot_binned_thumbnails(binned_thumbnails,
                           nrows=15,ncols=30,
                           vmin=0.1,vmax=1.5,
                           filename=None,
                           verticle = True,
                           **kwargs):
    from matplotlib.gridspec import GridSpec as gs
    if len(binned_thumbnails[0]) != nrows*ncols:
        raise ValueError('A fattened thumbnail should have a length of'+\
                         ' {} ({} X {}) but length {} array is given.'.format(nrows*ncols,
                                                                              nrows,
                                                                              ncols,
                                                                              binned_thumbnails[0]))
    aspect_ratio = ncols/nrows
    n_bins = len(binned_thumbnails)
    if verticle:
        fig = plt.figure(figsize=(aspect_ratio,n_bins))
        grids = gs(n_bins, 1, hspace=0.1)
        for i in range(n_bins):
            ax=fig.add_subplot(grids[i,:])
            ax.imshow(binned_thumbnails[i].reshape(nrows,ncols),vmin=vmin,vmax=vmax,aspect='auto',**kwargs)
            ax.axis('off')
    else:
        fig = plt.figure(figsize=(n_bins,aspect_ratio))
        grids = gs(1,n_bins,wspace=0.1)
        for i in range(n_bins):
            ax=fig.add_subplot(grids[:,i])
            ax.imshow(binned_thumbnails[i].reshape(nrows,ncols).T,vmin=vmin,vmax=vmax,aspect='auto',**kwargs)
            ax.axis('off')
    if filename is not None:
        plt.savefig(filename,**kwargs)
        plt.close()
    return fig
