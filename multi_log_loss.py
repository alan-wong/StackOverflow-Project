# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 22:49:56 2013

@author: alan
"""

from pandas import *
import numpy as np

def multi_log_loss(actual, pred, epsilon=1e-15):
    # compute log loss for each entry
    clip = np.clip(pred, epsilon, 1 - eps)
    actual = np.zeros(pred.shape)
    rows = actual.shape[0]
    actual[np.arange(rows), actual.astype(int)] = 1
    vsota = np.sum(actual * np.log(clip))
    return -1.0 / rows * vsota
    