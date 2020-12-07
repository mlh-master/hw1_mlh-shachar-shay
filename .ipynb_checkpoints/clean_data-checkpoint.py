# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:14:23 2019

@author: smorandv
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def rm_ext_and_nan(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A dictionary of clean CTG called c_ctg
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    CTG_features_copy=CTG_features.copy()
    del CTG_features_copy[extra_feature]
    c_ctg={id: pd.to_numeric(CTG_features_copy[id], errors = 'coerce').dropna() for id in CTG_features_copy}
    # --------------------------------------------------------------------------
    return c_ctg


def nan2num_samp(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A pandas dataframe of the dictionary c_cdf containing the "clean" features
    """
    c_cdf = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    CTG_features_copy = CTG_features.copy()
    del CTG_features_copy[extra_feature]
    c_cdf = {id: pd.to_numeric(CTG_features_copy[id], errors='coerce') for id in CTG_features_copy}
    for col in c_cdf:
        c_cdf_noNan=c_cdf[col].dropna()
        for id in c_cdf[col].index :
            if np.isnan(c_cdf[col][id])==True:
                c_cdf[col][id]=np.random.choice(c_cdf_noNan)

    # -------------------------------------------------------------------------
    return pd.DataFrame(c_cdf)


def sum_stat(c_feat):
    """

    :param c_feat: Output of nan2num_cdf
    :return: Summary statistics as a dicionary of dictionaries (called d_summary) as explained in the notebook
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    d_summary={}
    for id in c_feat:
       Q1=np.percentile(c_feat[id],25)
       Q3=np.percentile(c_feat[id],75)
       median=np.median(c_feat[id])
       upper_whisker=c_feat[id][c_feat[id]<=Q3+1.5*(Q3-Q1)].max()
       lower_whisker = c_feat[id][c_feat[id] >= Q1 - 1.5 * (Q3 - Q1)].min()
       d_summary[id]={ 'min':lower_whisker,'Q1':Q1, 'median':median , 'Q3':Q3, 'max':upper_whisker}


    # -------------------------------------------------------------------------
    return d_summary


def rm_outlier(c_feat, d_summary):
    """

    :param c_feat: Output of nan2num_cdf
    :param d_summary: Output of sum_stat
    :return: Dataframe of the dictionary c_no_outlier containing the feature with the outliers removed
    """
    c_no_outlier = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    for col in c_feat:
        index_min={index_min+1 for index_min, value in enumerate(c_feat[col]) if value<d_summary[col]['min']}
        c_no_outlier[col]=c_feat[col].drop(index_min)
        index_max = {index_max+1 for index_max, value in enumerate(c_feat[col]) if value > d_summary[col]['max']}
        c_no_outlier[col] = c_no_outlier[col].drop(index_max)


    # -------------------------------------------------------------------------
    return pd.DataFrame(c_no_outlier)




def phys_prior(c_cdf, feature, thresh):
    """

    :param c_cdf: Output of nan2num_cdf
    :param feature: A string of your selected feature
    :param thresh: A numeric value of threshold
    :return: An array of the "filtered" feature called filt_feature
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:-----------------------------
    c_cdf_copy=c_cdf.copy()
    index={index+1 for index, value in enumerate(c_cdf_copy[feature]) if value >thresh}
    filt_feature=c_cdf_copy[feature].drop(index)

    # -------------------------------------------------------------------------
    return filt_feature


def norm_standard(CTG_features, selected_feat=('LB', 'ASTV'), mode='none', flag=False):
    """

    :param CTG_features: Pandas series of CTG features
    :param selected_feat: A two elements tuple of strings of the features for comparison
    :param mode: A string determining the mode according to the notebook
    :param flag: A boolean determining whether or not plot a histogram
    :return: Dataframe of the normalized/standardazied features called nsd_res
    """
    x, y = selected_feat
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    nsd_res = {}
    if mode=='standard':
        for col in CTG_features:
            nsd_res[col]=(CTG_features[col]-CTG_features[col].mean())/CTG_features[col].std()
    elif mode=='MinMax':
        for col in CTG_features:
            nsd_res[col] = (CTG_features[col] - CTG_features[col].min()) / (CTG_features[col].max()-CTG_features[col].min())
    elif mode == 'mean':
        for col in CTG_features:
            nsd_res[col] = (CTG_features[col] - CTG_features[col].mean()) / (CTG_features[col].max()-CTG_features[col].min())
    else:
        nsd_res = CTG_features.copy()

    if flag==True:
        if mode=='none':
            nsd_res[x].hist(bins=100)
            plt.xlabel('Histogram %s '%(x))
            plt.ylabel('Count')
            plt.show()
            nsd_res[y].hist(bins=100)
            plt.xlabel('Histogram %s'%(y))
            plt.ylabel('Count')
            plt.show()
        else:
            nsd_res[x].hist(bins=100)
            plt.xlabel('Histogram %s after scaling: %s ' % (x,mode))
            plt.ylabel('Count')
            plt.show()
            nsd_res[y].hist(bins=100)
            plt.xlabel('Histogram %s after scaling: %s ' % (y,mode))
            plt.ylabel('Count')
            plt.show()


    # -------------------------------------------------------------------------
    return pd.DataFrame(nsd_res)