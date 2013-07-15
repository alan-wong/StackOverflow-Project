# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 13:43:27 2013

@author: alan
"""

import sys, csv
from math import log

from pandas import *
import numpy as np


test_file = r'h:\kaggle\train_October_9_2012.csv'
prior_test_file = r'h:\kaggle\train.csv'
predictions_file = r'h:\kaggle\basic_benchmark_Oct.csv'
prior_file = r'h:\kaggle\prior_benchmark.csv'
    
    
def multi_log_loss(actual, pred, epsilon=1e-15):
    # compute log loss for each entry
    clip = np.clip(pred, epsilon, 1 - epsilon)
    actual_arr = np.zeros(pred.shape)
    rows = actual.shape[0]
    actual_arr[np.arange(rows), actual.astype(int)] = 1

    vsota = np.sum(actual_arr * np.log(clip))
    return -1.0 / rows * vsota

def multiclass_log_loss(y_true, y_pred, eps=1e-15):
    """Multi class version of Logarithmic Loss metric.
    https://www.kaggle.com/wiki/MultiClassLogLoss

    idea from this post:
    http://www.kaggle.com/c/emc-data-science/forums/t/2149/is-anyone-noticing-difference-betwen-validation-and-leaderboard-error/12209#post12209

    Parameters
    ----------
    y_true : array, shape = [n_samples]
    y_pred : array, shape = [n_samples, n_classes]

    Returns
    -------
   loss : float
    """
    clip = np.clip(y_pred, eps, 1 - eps)
    actual = np.zeros(y_pred.shape)
    rows = actual.shape[0]
    print rows
    print np.arange(rows)
    print (y_true.astype(int))
    actual[np.arange(rows), y_true.astype(int)] = 1
    print actual
    vsota = np.sum(actual * np.log(clip))
    print vsota
    return -1.0 / rows * vsota 

def test():
    test_reader = read_csv(test_file,skiprows=1)
    p_reader = read_csv(predictions_file)
    
    # create 1- np array
    actual = test_reader[-1]
    print actual[:5]
    
def main():
    statuses = ['not a real question', 'not constructive', 'off topic', 'open', 'too localized']
        
    #test_reader = csv.reader( open( test_file ))
    test_reader = csv.reader( open( prior_test_file ))
    #p_reader = csv.reader( open( predictions_file ))
    p_reader = csv.reader( open( prior_file ))
    
    logs = []
    logs1 = 0.0
    n = 0
    test_line = test_reader.next()
    for p_line in p_reader:
        test_line = test_reader.next()
        #p_line.pop( 0 )	# get rid of post id
        #print test_line
        #print test_line[-1]
        n += 1
        
        status = test_line[-1]
        true_index = statuses.index( status )
        
        prediction_for_true = p_line[true_index]
        #print prediction_for_true
        #print "status %s, true index:%s, prediction %s" % (status, true_index, prediction_for_true)
        
        log_p = log( float( prediction_for_true ))
        #logs.append( log_p )
        logs1 += log_p 
    
    #logs = sum( logs )
    #print logs
    print logs1
    logloss = - logs1 / n * 1.0
    
    print "%s %s" % ( test_file, predictions_file )
    print logloss
    print
    
if __name__=="__main__":
    main()
#    a = np.array([(1,0),(1,0),(1,0),(0,1),(0,1),(0,1)])
#    p = np.array([(0.5, 0.5),(0.1, 0.9), (0.01, 0.99), (0.9, 0.1), (0.75, 0.25), (0.001, 0.999)])
#    print a
#    print p
#    y_true = np.array([0, 0, 0, 1, 1, 1])
#    y_pred = np.array([[0.5, 0.5], [0.1, 0.9], [0.01, 0.99],[0.9, 0.1], [0.75, 0.25], [0.001, 0.999]])
#    loss = multiclass_log_loss(y_true, y_pred) 
#    print loss
    #print(multi_log_loss(a, p))
    
    #test()