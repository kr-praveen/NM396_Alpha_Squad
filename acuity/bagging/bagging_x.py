""" 
1. Module Name: bagging_x (bagging.bagging_x)
2. Created on Sat Aug 01 12:07:42 2020
3. Author: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 12:07:42 2020
    
5. Synopsis: A module to return X vector after bagging

6. Functions Supported:
    a. get_X_vector(corpus, max_features):
        Input Parameters:
            i. corpus- List of pre-processed strings (corpus) - m rows
            ii. max_features- Maximum number of features to be considered during construction of bag of words
        Output Parameters:
            i. final_cv - Resultant CountVectorized matrix X of dimension (m, max_features)
            ii. models/countVectorier.pkl - Storing ount vectorizer object for future reference
"""
import pickle

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer

def get_X_vector(corpus, max_features):
    cv = CountVectorizer(max_features = max_features,ngram_range=(1,3))
    final_cv = cv.fit_transform(corpus).toarray()
    pickle.dump(cv, open('models/countVectorizer.pkl','wb'))
    return final_cv

