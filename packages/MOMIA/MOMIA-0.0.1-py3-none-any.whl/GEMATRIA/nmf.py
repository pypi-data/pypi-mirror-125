import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, NMF
import os, glob
import pickle as pk
from .plot import feature_plot
import pickle as pk

# now conduct NMF
def NMF_test(matrix,
             n_components=[20],
             rand_state=[47],
             alpha=[0.1],
             tol=[0.001],
             shape=(15,30),
             dst_folder=None,
             plot=True,
             save_plots=False,
             show_plots=False,
             save_models=True,
             **kwargs):

    # test whether input matrix has the right format
    if min(matrix.shape) <= 1:
        raise ValueError('For N x M matrix both N and M should be no smaller than 2.')
    if matrix.min() < 0:
        raise ValueError('Matrix should be non-negative.')
    if np.isnan(matrix).sum() > 0:
        raise ValueError('NaNs found in matrix')

    # create dst folder
    if dst_folder is not None:
        if not os.path.isdir(dst_folder):
            os.mkdir(dst_folder)
    parameter_dict = {}
    models = {}
    counter=0
    for n in list(n_components):
        for rd in list(rand_state):
            for a in list(alpha):
                for t in list(tol):
                    parameter_dict[counter] = {'n_components':n,
                                               'random_state':rd,
                                               'alpha':a,
                                               'tolerance':t}
                    counter+=1

    for k, par in parameter_dict.items():
        n, rd, a, t = par['n_components'], par['random_state'], par['alpha'], par['tolerance']
        model = NMF(n_components=n,
                    random_state=rd,
                    alpha=a,
                    tol=t,
                    **kwargs)
        w = model.fit_transform(matrix)
        h = model.components_
        residual = model.reconstruction_err_
        models[k] = {'model': model,
                     'encoding': w,
                     'basis': h,
                     'residual': residual,
                     'model_parameters': par}
        if plot:
            feature_plot(h, n,
                         shape=shape,
                         parameter_string='n_components: {}, rand_state: {}, alpha: {}, tolerance: {}'.format(n, rd, a, t),
                         dst_folder=dst_folder,
                         savefile=save_plots,
                         showplot=show_plots)


    if save_models:
        pk.dump(models, open('{}all_models.pk'.format(dst_folder), 'wb'))
    return models