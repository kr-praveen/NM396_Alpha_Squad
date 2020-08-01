# -*- coding: utf-8 -*-
"""
1. Module Name: basic (preprocessing.basic)
2. Created on Sat Aug 01 11:04:31 2020
3. Author: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 11:04:31 2020
    
5. Synopsis: Performs basic text pre-processing steps for natural language processing, like- data cleansing, removing symbols and digits, 
conversion to lowercase, stopword removal (English lang) and stemming etc

6. Functions Supported:
    a. preprocess_feedbacks(dataset, review_column):
        Input Parameters:
            i. dataset- Actual dataset that need to be pre-processed
            ii. review_column- Name or index of the column of dataset that contains reviews
        Output Parameters:
            i. Corpus- List with pre-processed reviews

7. Global variables accessed or modified: dataset
"""

# Importing the required packages and libraries
import re
import nltk
# In case stopwords are not downloaded, uncomment below given line
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Function: preprocess_feedbacks()
def preprocess_feedbacks(dataset, review_column):
    # corpus is a list to store resulting pre-processed reviews
    corpus = []
    # Applying pre-processing steps over all the reviews in the dataset using loop
    for i in range(0, len(dataset.index)):
        # Removing symbols and digits other than alphabets
        review = re.sub('[^a-zA-Z]', ' ', str(dataset[review_column][i]))
        # Converting in lowercase
        review = review.lower()
        # Converting in list because stopword removal function requires list as input
        review = review.split()
        # Creating object for stemming
        ps = PorterStemmer()
        # Performing Stop-word removal and Stemming on the individual review
        review = [ps.stem(word) for word in review if not word in set(stopwords.words('english_modified'))]
        # Joining the list words to make string
        review = ' '.join(review)
        # Adding the pre-processed review in corpus list
        corpus.append(review)
    # Returning corpus list     
    return corpus