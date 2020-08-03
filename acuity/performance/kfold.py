# -*- coding: utf-8 -*-
"""
1. Module Name: kfold (performance.kfold)
2. Created on Sat Aug 01 11:20:12 2020
3. Author: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 11:20:12 2020
    
5. Synopsis: Calculation of modal performance and accuracy metrics using K-Fold Cross Validation

6. Functions Supported:
    a. accuracy_score(classifier, X_train, y_train, n_cv):
        Input Parameters:
            i. classifier- ML modal on which K-Fold Cross validation is to be applied
            ii. X-train- Matrix of features for training data
            iii. y_train- Result vector for training data
            iv. n_cv- Number of cross-validations
        Output Parameters:
            i. accuracies.mean()- Mean of accuracy scores
            ii. accuracies.std()- Standard deviation of accuracy scores
            
    b. accuracy_macro(classifier, X_train, y_train, n_cv):
        Input Parameters:
            i. classifier- ML modal on which K-Fold Cross validation is to be applied
            ii. X-train- Matrix of features for training data
            iii. y_train- Result vector for training data
            iv. n_cv- Number of cross-validations
        Output Parameters:
            i. precision.mean()- Average precision score using K-Fold CV
            ii. recall.mean()- Average recall score using K-Fold CV
            iii. fmeasure.mean()- Average f-measure score using K-Fold CV
            
    c. accuracy_micro(classifier, X_train, y_train, n_cv):
        Input Parameters:
            i. classifier- ML modal on which K-Fold Cross validation is to be applied
            ii. X-train- Matrix of features for training data
            iii. y_train- Result vector for training data
            iv. n_cv- Number of cross-validations
        Output Parameters:
            i. precision.mean()- Average precision score using K-Fold CV
            ii. recall.mean()- Average recall score using K-Fold CV
            iii. fmeasure.mean()- Average f-measure score using K-Fold CV
            
    d. accuracy_weighted(classifier, X_train, y_train, n_cv):
        Input Parameters:
            i. classifier- ML modal on which K-Fold Cross validation is to be applied
            ii. X-train- Matrix of features for training data
            iii. y_train- Result vector for training data
            iv. n_cv- Number of cross-validations
        Output Parameters:
            i. precision.mean()- Average precision score using K-Fold CV
            ii. recall.mean()- Average recall score using K-Fold CV
            iii. fmeasure.mean()- Average f-measure score using K-Fold CV
                  
    'micro':
        Calculate metrics globally by counting the total true positives, false negatives and false positives.

    'macro':
        Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.

    'weighted':
        Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label). 
        This alters ‘macro’ to account for label imbalance; it can result in an F-score that is not between precision and recall.

7. Global variables accessed or modified: classifier
"""

# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score

def accuracy_score(classifier, X_train, y_train, n_cv):
    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = n_cv)
    return accuracies.mean(), accuracies.std()

def accuracy_macro(classifier, X_train, y_train, n_cv):
    precision = cross_val_score(classifier, X_train, y_train, cv=n_cv, scoring='precision_macro')
    recall = cross_val_score(classifier, X_train, y_train, cv=n_cv, scoring='recall_macro')
    fmeasure = cross_val_score(classifier, X_train, y_train, cv=n_cv, scoring='f1_macro')
    return precision.mean(), recall.mean(), fmeasure.mean()

def accuracy_micro(classifier, X_train, y_train, n_cv):
    precision = cross_val_score(classifier, X_train, y_train, cv=n_cv, scoring='precision_micro')
    recall = cross_val_score(classifier, X_train, y_train, cv=n_cv, scoring='recall_micro')
    fmeasure = cross_val_score(classifier, X_train, y_train, cv=n_cv, scoring='f1_micro')
    return precision.mean(), recall.mean(), fmeasure.mean()

def accuracy_weighted(classifier, X_train, y_train, n_cv):
    precision = cross_val_score(classifier, X_train, y_train, cv=n_cv, scoring='precision_weighted')
    recall = cross_val_score(classifier, X_train, y_train, cv=n_cv, scoring='recall_weighted')
    fmeasure = cross_val_score(classifier, X_train, y_train, cv=n_cv, scoring='f1_weighted')
    return precision.mean(), recall.mean(), fmeasure.mean()