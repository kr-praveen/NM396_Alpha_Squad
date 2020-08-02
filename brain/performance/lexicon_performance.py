# -*- coding: utf-8 -*-
"""
1. Module Name: lexicon_performance (preprocessing.lexicon_performance)
2. Created on Sat Aug 01 2020
3. Author: Team Alpha Squad

4. Modification History: NIL
    
5. Synopsis: Checking the accuracy (performance) through Hybrid Approach (Lexicon based approach + ML based approach)

6. Functions Supported:
    a. list_ratings_attributes(reviews):
        Input Parameters:
            i. reviews- List of review strings
        Output Parameters:
            i. ratings- A list of sentiments(ratings) over the string of the reviews list
    
    b. check_hybrid_performance(file_name, column_review, column_rating, size):
        Input Parameters:
            i. file_name- filename of the json file on which performance analysis is to be done. 
                            Note that the file should be stored in "main/files" directory.
            ii. column_review- Name of the column that contains review strings
            iii. column_rating- Name of the column that contains rating strings
            iv. size- Size of dataset on which analysis is to be performed
        Output Parameters:
            i. accuracy- Accuracy computed
            ii. precision- Precision computed
            iii. recall- Recall computed
            iv. fmeasure- F-measure computed
"""

from pandas import read_json
from performance.accuracy_measures import accuracy_macro
from main import hybrid_predict
from sklearn.metrics import confusion_matrix
from main.resources.progress_bar import printProgressBar

def list_ratings_attributes(reviews):
    ratings = []
    i=0
    total = len(reviews)
    printProgressBar(0, total, prefix = 'Finding:', suffix = 'Complete', length = 50)
    model = hybrid_predict.Hybrid_rate()
    for line in reviews:
        rating = model.get_hybrid_rating(line)
        ratings.append(rating)
        i+=1
        printProgressBar(i, total, prefix = 'Finding:', suffix = 'Complete', length = 50)  
        
    return ratings

def check_hybrid_performance(file_name, column_review, column_rating, size, start = 0):
    dataset = read_json('main/files/'+file_name, lines=True)
    dataset = dataset.sample(frac=1).reset_index(drop=True)
    dataset = dataset[start:start + size]
    reviews = dataset[column_review].tolist()
    actual_rating = dataset[column_rating].tolist()
    prediction_rating = list_ratings_attributes(reviews)
    
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(actual_rating,prediction_rating)
    
    precision, recall, fmeasure = accuracy_macro(actual_rating, prediction_rating)
    cm = confusion_matrix(actual_rating, prediction_rating)
    return accuracy, precision, recall, fmeasure, cm

# Sample Test Case:
acu, pre, rec, fea, cmh = check_hybrid_performance(file_name="Software.json", column_review="reviewText", column_rating="overall", size=500, start =0)