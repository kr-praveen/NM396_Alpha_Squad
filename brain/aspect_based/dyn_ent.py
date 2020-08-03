"""
Author : Team Alpha Squad
Optional Module for entity extraction
Input : list of reviews
Output : list of entities
"""

import nltk
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
from nltk.corpus import stopwords

adjectives = open("resources/positive-words.txt").readlines()
adjectives.extend(open("resources/negative-words.txt").readlines())
adjectives = [word.rstrip("\n").lower().strip() for word in adjectives]

def return_entity(reviews):
  
    strings = []
    
    
    for review in reviews:
        sentences = sent_tokenize(review)
        for sentence in sentences:
            words = word_tokenize(sentence)
            tagged = nltk.pos_tag(words)
            
            namedEnt = nltk.ne_chunk(tagged)
            for i in namedEnt:
                for j in range(3):
                    try:
                        if len(i[j][0])>1:
                            if j == 0:
                                strings.append(str(i[j][0]).lower()) 
                            else :
                                strings[-1] = strings[-1] + " " + str(i[j][0]).lower()
                    except:            
                        break
                   
    strings = [word for word in strings if nltk.pos_tag([str(word)])[0][1]=="NN" and word not in adjectives and len(word)>2 and word not in stopwords.words("english")]          
    counter = Counter(strings) 
    
    entity = counter.most_common(20)            
    
    entity = [i[0] for i in entity]
    
    return entity

reviews = ["""camera is very poor.
device set-up is also difficult.
battery draining fast.
no replacement policy.
please don't buy this phone
In this price range you can go for Samsung galaxy M30s. """]
#reviews = list(pd.read_json("files/n_entity.json", lines = True)['reviewText'][:])
entity = return_entity(reviews)