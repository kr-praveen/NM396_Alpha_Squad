
"""
Desc   : A file to generate rating of a user review by lexical analysis of good and bad words in the review

How To Use : e.g. get_rating("this page is really not nice") 
                    OUTPUT : 3
               
                2. get_rating("this page is best one can see")
                Out[95]: 5
                
1. Module Name: lexical_predict (main.lexical_predict)
2. Created on Sat Aug 01 2020
3. Author(s): Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 2020
    
    
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
from preprocessings.basic import preprocess_lemm_string
from preprocessings.string_to_eng import convert_to_english
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model


extra_words = stopwords.words("english") 
negatives = ['ain','dont','didnt','aren', "aren't", 'couldn','wasnot','wasnt',"wasn't", "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'don', "don't", 'no', 'nor', 'not','wouldnt','shouldnt','isnt','arent','wasnt','werent','willnt','shallnt','couldnt','cant','mightnt','neednt','mustnt',"n't"]
extra_words = [words for words in extra_words if words not in negatives]

class Hybrid_rate:
    def __init__(self, lang = " ", model_file="TD20200309210544"):
        self.lang = lang
        self.model = load_model('static/DBAlpha/TrainingDB/Models/' + model_file+'.h5')
        self.token = pickle.load(open('static/DBAlpha/TrainingDB/Models/TOKEN_' + model_file+'.pkl', 'rb'))
        print("Used Model: ", model_file)
        try:
            self.positive_list = self.process_list(self.return_to_list("resources/positive-words.txt"))
            self.negetive_list = self.process_list(self.return_to_list("resources/negative-words.txt"))
            
        except:
            self.positive_list = self.process_list(self.return_to_list("main/resources/positive-words.txt"))
            self.negetive_list = self.process_list(self.return_to_list("main/resources/negative-words.txt"))
            
            
    def return_to_list(self, file_name):
        return open(file_name).readlines()
    
    def process_list(self, list_name):
        for st in list_name:
            st = st.rstrip("\n").lower().strip()
        return list_name
    
    def check_polarity(self, review, word, index_, pol):
      
        cutoff=2
        if index_<2:
            cutoff=1
        if index_<1:
            return pol
        for i in range(index_-cutoff,index_):
            if review[i].lower() in negatives:
                pol=-1*pol
        return pol
    
    def convert_to_rating(self, pos, neg):
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
        

    def get_rnn_rating(self, review):
        if self.lang == "multi":
            # Converting review to english (If in other language)
            review = convert_to_english(review)
        review_tokens = word_tokenize(str(review))
        corpus_for_string = preprocess_lemm_string(review_tokens)
        X_string = self.token.texts_to_sequences(corpus_for_string)
        feature = pad_sequences(X_string, 150)
        output = self.model.predict(feature)
        max_ = output[0][0]
        for j in range(5):
            if output[0][j]>=max_:
                max_ = output[0][j]
                rating = j+1
        return rating
    
    def get_rnn_output(self, review):
        review_tokens = word_tokenize(str(review))
        corpus_for_string = preprocess_lemm_string(review_tokens)
        X_string = self.token.texts_to_sequences(corpus_for_string)
        feature = pad_sequences(X_string, maxlen = 150)
        return self.model.predict(feature)


    
    def get_hybrid_rating(self, review):
        
        if self.lang == "multi":
            # Converting review to english (If in other language)
            review = convert_to_english(review)
        rnn_output = self.get_rnn_output(review)
        lex_rating = self.get_lexical_rating(review)
        
        max_ = rnn_output[0][0]
        for j in range(5):
            if rnn_output[0][j]>=max_:
                max_ = rnn_output[0][j]
                rating = j+1
        
               
        if max_ < 0.7:
            new_max = -1 
            for i in range(5):
                if i == rating - 1:
                    continue
                if rnn_output[0][i]>=new_max:
                    new_max = rnn_output[0][i]
                    new_rating = i+1 
            
        
            if lex_rating < 3:
                if rating!=1:
                    if new_rating < rating:
                        rating = new_rating
                    
            elif lex_rating >3:
                if rating!=5:
                    if new_rating > rating:
                        rating = new_rating
    
        return rating
    
    def get_lexical_rating(self,user_lines):
        
        if self.lang == "multi":
            # Converting review to english (If in other language)
            user_lines = convert_to_english(user_lines)
        user_review = word_tokenize(str(user_lines).lower())
        user_review = [word for word in user_review if not word in extra_words]
        pos = 0
        neg = 0
        ind = 0
        for word in user_review:
            for pos_word in self.positive_list:
                if word==pos_word.rstrip("\n"):
                    polarity = self.check_polarity(user_review, word, ind, 1)
                    if polarity == 1:
                        pos+=1
                    else:
                        neg+=1
            for neg_word in self.negetive_list:
                if word==neg_word.rstrip("\n"):
                    polarity = self.check_polarity(user_review, word, ind, -1)
                    if polarity == -1:
                        neg+=1
                    else: 
                        pos+=1
            ind +=1
        
        rating = self.convert_to_rating(pos,neg)

        return rating