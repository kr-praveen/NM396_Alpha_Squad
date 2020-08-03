# -*- coding: utf-8 -*-
"""
1. Module Name: basic (preprocessing.basic)
1. Module Name: basic (preprocessing.basic)
2. Created on Sat Aug 01 11:04:31 2020
3. Author: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 11:04:31 2020
    
5. Synopsis: Performs basic text pre-processing steps for natural language processing, like- data cleansing, removing symbols and digits, 
conversion to lowercase, stopword removal (English lang) and stemming etc

6. Functions Supported:
    a. preprocess_stem_dataset(dataset, review_column):
        Uses Stemming
        Input Parameters:
            i. dataset- Actual dataset that need to be pre-processed
            ii. review_column- Name or index of the column of dataset that contains reviews
        Output Parameters:
            i. Corpus- List with pre-processed reviews

    b. preprocess_stem_string(review_string):
        Uses Stemming
        Input Parameters:
            i. review_string- String on which pre-processing is to be done
        Output Parameters:
            i. Corpus- List with pre-processed string
            
    c. preprocess_lemm_dataset(dataset, review_column):
        Uses Lemmatization
        Input Parameters:
            i. dataset- Actual dataset that need to be pre-processed
            ii. review_column- Name or index of the column of dataset that contains reviews
        Output Parameters:
            i. Corpus- List with pre-processed reviews

    d. preprocess_lemm_string(review_string):
        Uses Lemmatization
        Input Parameters:
            i. review_string- String on which pre-processing is to be done
        Output Parameters:
            i. Corpus- List with pre-processed string
    
    e. file_to_list()
        input - path of the file
        output - a list of lines in that file

7. Global variables accessed or modified: dataset
"""

# Importing the required packages and libraries
import re
from nltk.corpus import stopwords
import numpy as np
from main.resources.progress_bar import printProgressBar 

# Exclude negetions from stopwords
extra_words = stopwords.words('english')
negatives = ['ain','dont','didnt','aren', "aren't", 'couldn','wasnot','wasnt',"wasn't", "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'don', "don't", 'no', 'nor', 'not','wouldnt','shouldnt','isnt','arent','wasnt','werent','willnt','shallnt','couldnt','cant','mightnt','neednt','mustnt']
extra_words = [words for words in extra_words if words not in negatives]

# Function: preprocess_feedbacks()
def preprocess_stem_dataset(dataset, review_column):
    # corpus is a list to store resulting pre-processed reviews    
    from nltk.stem.porter import PorterStemmer
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
        review = [ps.stem(word) for word in review if not word in set(extra_words)]
        # Joining the list words to make string
        review = ' '.join(review)
        # Adding the pre-processed review in corpus list
        corpus.append(review)
    # Returning corpus list     
    return corpus

# Function: preprocess_string()
def preprocess_stem_string(review_string):
    # corpus is a list to store resulting pre-processed reviews    
    from nltk.stem.porter import PorterStemmer
    corpus = []
    # Removing symbols and digits other than alphabets
    review = re.sub('[^a-zA-Z]', ' ', str(review_string))
    # Converting in lowercase
    review = review.lower()
    # Converting in list because stopword removal function requires list as input
    review = review.split()
    # Creating object for stemming
    ps = PorterStemmer()
    # Performing Stop-word removal and Stemming on the individual review
    review = [ps.stem(word) for word in review if not word in set(extra_words)]
    # Joining the list words to make string
    review = ' '.join(review)
    # Adding the pre-processed review in corpus list
    corpus.append(review)
    # Returning corpus list  
    return corpus

# Function: preprocess_feedbacks()
def preprocess_lemm_dataset(dataset, review_column):
    # corpus is a list to store resulting pre-processed review    
    from nltk.stem import WordNetLemmatizer
    corpus = []
    print("")
    printProgressBar(0, len(dataset.index), prefix = 'Make Corpus:', suffix = 'Complete', length = 50)
    # Applying pre-processing steps over all the reviews in the dataset using loop
    for i in range(0, len(dataset.index)):
        # Removing symbols and digits other than alphabets
        review = re.sub('[^a-zA-Z]', ' ', str(dataset[review_column][i]))
        # Converting in lowercase
        review = review.lower()
        # Converting in list because stopword removal function requires list as input
        review = review.split()
        # Creating object for stemming
        lem = WordNetLemmatizer()
        # Performing Stop-word removal and Stemming on the individual review
        review = [lem.lemmatize(word) for word in review if not word in set(extra_words)]
        # Joining the list words to make string
        review = ' '.join(review)
        # Adding the pre-processed review in corpus list
        corpus.append(review)
        
        printProgressBar(i, len(dataset.index), prefix = 'Making Corpus:', suffix = 'Complete', length = 50)
    # Returning corpus list     
    return corpus


# Function: preprocess_string()
def preprocess_lemm_string(review_string):
    # corpus is a list to store resulting pre-processed reviews 
    corpus = []
    from nltk.stem import WordNetLemmatizer
    # Removing symbols and digits other than alphabets
    review = re.sub('[^a-zA-Z]', ' ', str(review_string))
    # Converting in lowercase
    review = review.lower()
    # Converting in list because stopword removal function requires list as input
    review = review.split()
    # Creating object for stemming
    lem = WordNetLemmatizer()
    # Performing Stop-word removal and Stemming on the individual review
    review = [lem.lemmatize(word) for word in review if not word in set(extra_words)]
    # Joining the list words to make string
    review = ' '.join(review)
    # Adding the pre-processed review in corpus list
    corpus.append(review)
    # Returning corpus list  
    return corpus



def file_to_list(path):
    
    def return_to_list( file_name):
        return open(file_name).readlines()
    
    def process_list( list_name):
        for ind, st in enumerate(list_name):
            list_name[ind] = st.rstrip("\n").lower().strip()
        return list_name
    
    return process_list(return_to_list(path))

