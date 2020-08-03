"""
1. Module Name: lexical_predict (main.lexical_predict)
2. Created on Sat Aug 01 01:11:48 2020

3. Author: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 01:11:48 2020
    
5. Synopsis: Executes the sentiment analysis process with hybrid approach (ML based approach + Lexicon based approach)

6. Functions Supported:
    Class: Lexical_rate
    Methods:
        a. return_to_list(file_name):
            Input Parameters:
                file_name- Name of the file with location
            Output Parameters:
                List of strings
                
        b. process_list(list_name):
            Input Parameters:
                list_name- Name of the list to be processed
            Output Parameters:
                list with basic preprocessing (like- stripping '\n' and converting to lower case )
        
        c. check_polarity(review, word, pol):
            Input Parameters:
                i. review- Review String
                ii. word- Word which is to be analysed
                iii. index_-Index of the word
                iv. pol- Initial polarity (-1 for negative, +1 for positive)
            Output Parameters:
                i. pol- Final polarity
        
        d. give_rating(pos, neg):
            Input Parameters:
                i. pos- number of positive words
                ii. neg- number of negative words
            Output Parameters:
                Returns rating by appling Lexicon-based approach
        
        e. get_rating_supervised(review):
            Input Parameters:
                i. review- review to be processed for ANN Based sentiment analysis
            Output Parameters:
                ii. rating- Rating as analysed by ANN
        
        f. get_rating(user_lines):
            Input Parameters:
                i. review- review to be processed for sentiment analysis
            Output Parameters:
                ii. rating- Rating as analysed by Hybrid approach (ML based + Lexicon based)

7. Global variables accessed or modified: N/A
"""

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pickle
import sys
sys.path.append('../')
from preprocessing.basic import preprocess_lemm_string
try:
    model = pickle.load(open('models/model.pkl', 'rb'))
    cv = pickle.load(open('models/countVectorizer.pkl', 'rb'))
except :
    model = pickle.load(open('main/models/model.pkl', 'rb'))
    cv = pickle.load(open('main/models/countVectorizer.pkl', 'rb'))

extra_words = stopwords.words("english")


class Lexical_rate:
    def return_to_list(self, file_name):
        return open(file_name).readlines()
    
    def process_list(self, list_name):
        for st in list_name:
            st = st.rstrip("\n").lower().strip()
        return list_name
    
    def check_polarity(self, review, word, index_, pol):
        negatives = ['ain','dont','didnt','aren', "aren't", 'couldn', "n't", "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'don', "don't", 'no', 'nor', 'not','wouldnt','shouldnt','isnt','arent','wasnt','werent','willnt','shallnt','couldnt','cant','mightnt','neednt','mustnt']
        cutoff=2
        if index_<1:
            return pol
        if index_<2:
            cutoff=1
        for i in range(index_-cutoff,index_):
            if review[i].lower() in negatives:
                pol=-1*pol
        return pol
    
    def give_rating(self, pos, neg):
        if pos==neg:
            return 3
        elif pos/2>neg:
            return 5
        elif neg/2>pos:
            return 1
        elif pos>neg:
            return 4
        else:
            return 2
    
    def get_rating_supervised(self,review):
        rating = 0
        review_tokens = word_tokenize(review)
        corpus_for_string = preprocess_lemm_string(review_tokens)
        X_string = cv.transform(corpus_for_string)
        output = model.predict(X_string)
        max_ = output[0][0]
        for j in range(5):
            if output[0][j]>=max_:
                max_ = output[0][j]
                rating = j+1
        return rating

     
    
    def get_rating(self,user_lines):
        
        try:
            positive_list = self.process_list(self.return_to_list("resources/positive-words.txt"))
            negetive_list = self.process_list(self.return_to_list("resources/negative-words.txt"))
            
        
        except:
            positive_list = self.process_list(self.return_to_list("main/resources/positive-words.txt"))
            negetive_list = self.process_list(self.return_to_list("main/resources/negative-words.txt"))
        
        user_review = word_tokenize(str(user_lines).lower())
        user_review = [word for word in user_review if not word in extra_words]
        pos = 0
        neg = 0
        ind = 0
        for word in user_review:
            for pos_word in positive_list:
                if word==pos_word.rstrip("\n"):
                    polarity = self.check_polarity(user_review, word, ind, 1)
                    if polarity == 1:
                        pos+=1
                    else:
                        neg+=1
            for neg_word in negetive_list:
                if word==neg_word.rstrip("\n"):
                    polarity = self.check_polarity(user_review, word, ind, -1)
                    if polarity == -1:
                        neg+=1
                    else: 
                        pos+=1
            ind +=1
        
        rating = self.give_rating(pos,neg)
        
        if pos==neg:
            rating = self.get_rating_supervised(user_lines)
        
        elif pos>neg:
            if neg/pos > 0.7:
                rating = self.get_rating_supervised(user_lines)
            else :
                rating = self.give_rating(pos,neg)
        else :
            if pos/neg > 0.7:
                rating = self.get_rating_supervised(user_lines)
            else :
                rating = self.give_rating(pos,neg)
        #rating = self.get_rating_supervised(user_lines)
        return rating