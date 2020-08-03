# -*- coding: utf-8 -*-
"""
1. Module Name: lexicon_performance (preprocessing.lexicon_performance)
2. Created on Mon Jan 20 2020
2. Created on Sat Aug 01 11:23:51 2020
3. Author: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 11:23:51 2020
    
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
import lexical_predict
from pandas import read_json
from sys import path
path.append("../")
from performance.accuracy_measures import accuracy_macro

def list_ratings_attributes(reviews):
    ratings = []
    i=0
    model = lexical_predict.Lexical_rate()
    for line in reviews:
        try:
            current_rating = model.get_rating(line)
            ratings.append(current_rating)
        except:
            ratings.append(3)
        if i%100==0:
            print(i)
        i+=1   
    return ratings

def check_hybrid_performance(file_name, column_review, column_rating, size):
    dataset = read_json('files/'+file_name, lines=True)
    dataset = dataset[:size]
    reviews = dataset[column_review].tolist()
    actual_rating = dataset[column_rating].tolist()
    prediction_rating = list_ratings_attributes(reviews)
    
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(actual_rating,prediction_rating)
    
    precision, recall, fmeasure = accuracy_macro(actual_rating, prediction_rating)
    return accuracy, precision, recall, fmeasure

# Sample Test Case:
# check_hybrid_performance(file_name="uniform_json.json", column_review="review", column_rating="rating", size=100)