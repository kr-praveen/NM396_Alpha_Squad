# -*- coding: utf-8 -*-
"""
1. Module Name: accuracy_measures (performance.accuracy_measures)
2. Created on Sat Aug 01 11:10:43 2020
3. Author: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 11:10:43 2020
    
5. Synopsis: Calculation of modal performance with basic

6. Functions Supported:
    a. cm_binary_accuracy(cm):
        Input Parameters:
            i. cm- Confusion Metric (Binary Class, Two categories)
            iv. n_cv- Number of cross-validations
        Output Parameters:
            i. accuracy- Accuracy Score
            ii. precision- Precision score
            iii. recall- Recall score
            iv. fmeasure- F-measure score
            
    b. accuracy_macro(y_test, y_pred):
        Input Parameters:
            i. y_test- Actual result vector obtained from test dataset
            ii. y_pred- Predicted result vector obtained from test dataset
        Output Parameters:
            i. precision- Precision score
            ii. recall- Recall score
            iii. fmeasure- F-measure score
            
    b. accuracy_micro(y_test, y_pred):
        Input Parameters:
            i. y_test- Actual result vector obtained from test dataset
            ii. y_pred- Predicted result vector obtained from test dataset
        Output Parameters:
            i. precision- Precision score
            ii. recall- Recall score
            iii. fmeasure- F-measure score
            
    b. accuracy_weighted(y_test, y_pred):
        Input Parameters:
            i. y_test- Actual result vector obtained from test dataset
            ii. y_pred- Predicted result vector obtained from test dataset
        Output Parameters:
            i. precision- Precision score
            ii. recall- Recall score
            iii. fmeasure- F-measure score
                  
    'micro':
        Calculate metrics globally by counting the total true positives, false negatives and false positives.

    'macro':
        Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.

    'weighted':
        Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label). 
        This alters ‘macro’ to account for label imbalance; it can result in an F-score that is not between precision and recall.

7. Global variables accessed or modified: none
"""

from sklearn.metrics import recall_score, precision_score, f1_score

def cm_binary_accuracy(cm):
    accuracy = (cm[0][0]+cm[1][1])/(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1])
    precision = cm[1][1]/(cm[1][1]+cm[0][1])
    recall = cm[1][1]/(cm[1][1]+cm[1][0])
    fmeasure = (2*precision_score*recall_score)/(precision_score+recall_score)
    return accuracy, precision, recall, fmeasure

def accuracy_macro(y_test, y_pred):
    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    fmeasure = f1_score(y_test, y_pred, average='macro')
    return precision, recall, fmeasure

def accuracy_micro(y_test, y_pred):
    precision = precision_score(y_test, y_pred, average='micro')
    recall = recall_score(y_test, y_pred, average='micro')
    fmeasure = f1_score(y_test, y_pred, average='micro')
    return precision, recall, fmeasure

def accuracy_weighted(y_test, y_pred):
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    fmeasure = f1_score(y_test, y_pred, average='weighted')
    return precision, recall, fmeasure