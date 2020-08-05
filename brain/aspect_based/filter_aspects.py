"""
Author: Team Alpha Squad
Date  : Sat 01 August 2020
Input : List of reviews called as corpus

Attribute object has filtered_attributes that containt the dynamically found attribute list
"""

   
from nltk.corpus import wordnet
import sys
sys.path.append("../")
from nltk.tokenize import word_tokenize
from preprocessings.basic import file_to_list

def return_all_synonyms(word_list):
    dict_word = {key: set() for key in word_list}

    for word in word_list:
        for syn in wordnet.synsets(word):
        		for l in syn.lemmas():
        			dict_word[word].add(l.name())
    
    word_list = []
    for key in dict_word:
        word_list.append(list(dict_word[key]))
        
    return word_list


class Attributes:
  
    def __init__(self,corpus):
        self.attributes_ = file_to_list("main/resources/attribute_list.txt") 
        all_attributes = return_all_synonyms(self.attributes_)
        self.filtered_attributes = self.select_attributes(corpus, all_attributes)
    
    def select_attributes(self, corpus, all_attributes):
            dict_att = {key: 0 for key in self.attributes_}
            for review in corpus:
                words = word_tokenize(str(review))
                
                for word in words:
                    for i in range(len(self.attributes_)):
                        if word in all_attributes[i]:
                            dict_att[self.attributes_[i]]+=1
            dict_att1 = sorted(dict_att.items(), key=lambda x: x[1], reverse = True)
            dict_att1 = dict_att1[:5]
            return [tuple_[0] for tuple_ in dict_att1]
