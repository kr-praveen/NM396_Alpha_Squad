"""
Author: Team Alpha Squad
Optional Module for aspect based

"""
  
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from nltk.tag import pos_tag
from sent_pred import Entity
from make_n_entites import make_entity_wise_json

# Making entity wise json
make_entity_wise_json("Appliances.json", 2)


def get_aspect_list(reviews):
    adjectives = open("resources/positive-words.txt").readlines()
    adjectives.extend(open("resources/negative-words.txt").readlines())
    
    adjectives = [word.rstrip("\n").lower().strip() for word in adjectives]
    
    reviews = reviews[:2000]
    aspects = []
    
    for review in reviews:
        sentences = sent_tokenize(str(review))
        for sentence in sentences:
            words = word_tokenize(str(sentence))
            for word in words:
                if word in adjectives:
                    ind = words.index(word)
                    try:
                        if sentence[ind+1]!='.':
                            aspects.extend([words[ind+1]])
                        else:
                            aspects.append(words[ind-1])
                    except:
                        pass
                    
    tokenizer = Tokenizer(100, lower=True, char_level=False)
    tokenizer.fit_on_texts(aspects)
    tokenizer.texts_to_sequences(aspects)
    aspects = list(tokenizer.word_index)
    aspects = [word for word in aspects if pos_tag([str(word)])[0][1]=="NN" and len(word)>2 and word not in adjectives and word not in stopwords.words("english")]
    aspects = aspects[:10]
    
    return aspects



dataset = pd.read_json("files/n_entity.json", lines = True)
reviews = list(dataset['reviewText'])

aspects = get_aspect_list(reviews)
