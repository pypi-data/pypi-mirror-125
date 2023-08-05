#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd

def conf_matrix(_df, pred, target):
    df = _df.copy()
    num_uni = pd.DataFrame(df[pred].describe(percentiles=
                                               [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
                                                0.7, 0.8, 0.9, 0.95, 0.99])).transpose()
    df['decile_pred'] = np.where(df[pred] <= num_uni.iloc[:, 5][0], 1, np.where(
        df[pred] <= num_uni.iloc[:, 6][0], 2, np.where(
            df[pred] <= num_uni.iloc[:, 7][0], 3, np.where(
                df[pred] <= num_uni.iloc[:, 8][0], 4, np.where(
                    df[pred] <= num_uni.iloc[:, 9][0], 5, np.where(
                        df[pred] <= num_uni.iloc[:, 10][0], 6, np.where(
                            df[pred] <= num_uni.iloc[:, 11][0], 7, np.where(
                                df[pred] <= num_uni.iloc[:, 12][0], 8, np.where(
                                    df[pred] <= num_uni.iloc[:, 13][0], 9, 10)))))))))
    df = df.sort_values(pred, ascending=False)
    mat1 = df.groupby("{}_{}".format('decile', pred)).agg({
        pred: {'count', 'max'},
        target: 'sum'}).sort_values(
        "{}_{}".format('decile', pred), ascending=False).droplevel(0, axis=1).reset_index()
    mat1 = mat1.rename(columns={'count': 'cnt', 'max': "{}_{}".format('max', pred), 'sum': 'resp'})
    mat1['non_resp'] = mat1['cnt'] - mat1['resp']
    mat1['cumresp'] = mat1.resp.cumsum()
    mat1['cumcnt'] = mat1.cnt.cumsum()
    mat1['resp_rate'] = (mat1['cumresp'] / mat1['cumcnt']) * 100
    mat1['lift'] = mat1['resp_rate']/((mat1['resp'].sum()/mat1['cnt'].sum())*100)
    mat1['tp'] = mat1.cumresp
    mat1['fp'] = mat1.cumcnt - mat1.cumresp
    mat1['tn'] = (mat1.cnt.sum() - mat1.resp.sum()) - mat1.fp
    mat1['fn'] = mat1.resp.sum() - mat1.tp
    mat1['precision'] = (mat1.tp / (mat1.tp + mat1.fp)) * 100
    mat1['recall'] = (mat1.tp / mat1.resp.sum()) * 100
    mat1['fscore'] = (2 * mat1.precision * mat1.recall) / (mat1.precision + mat1.recall)
    mat1['accuracy'] = ((mat1.tp + mat1.tn) / mat1.cnt.sum()) * 100
    mat1['ks'] = (mat1.tp / mat1.resp.sum()) * 100 - (mat1.fp / (mat1.cnt.sum() - mat1.resp.sum())) * 100
    return mat1

