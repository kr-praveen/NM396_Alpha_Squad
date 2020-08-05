"""
1. Module Name: model_suggestion
2. Created on Mon Aug 03 2020
3. Author: Taem Alpha Squad

4. Modification History:
    NIL
       
5. Synopsis: Module to predict the suggestions in a given list of string
    
6. Functions Supported:
    a.get_suggestive_words():
        function to get "suggestive words" that helps to identify a suggestion
        
    b. predict_suggestions(reviews)
        i. Input : 
            i.   reviews : a list of reviews (list of strings)
            ii.  return_type: can be "ist" or "json" string
           
        ii. Output:
            i.   suggestions: list of suggestions (list of strings)(not entity wise)
                                or
            ii.  json string (entity wise)
        
7. Global variables accessed or modified: 
    i. model : suggestive model saved by "model_suggestion.py"
    ii. token: tokenizer saved by same file
"""

from preprocessings.basic import preprocess_lemm_string
from nltk.tokenize import sent_tokenize
import pickle
import warnings
from preprocessings.basic import file_to_list
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
warnings.filterwarnings("ignore")
#model = pickle.load(open('static/DBAlpha/TrainingDB/Models/suggestion.pkl', 'rb'))
#token = pickle.load(open('static/DBAlpha/TrainingDB/Models/suggestion_token.pkl', 'rb'))
import json, re
import pandas as pd

def predict_suggestions(file_name,review_label = "reviewText", entity_label= 'asin', return_type = "json"):
    print("Extracting Suggestions....")
    dataset = pd.read_json(r"static/DBAlpha/FeedbackDB/Files/"+file_name, lines = True)
    model = load_model(r'static/DBAlpha/TrainingDB/Models/suggestion.h5')
    token = pickle.load(open(r'static/DBAlpha/TrainingDB/Models/suggestion_token.pkl', 'rb'))
    suggestion = []
    entity = []
    reviews = dataset[review_label]
    suggestive_words = file_to_list("main/resources/suggestive-words.txt")
    for ind, review in enumerate(reviews):
        sentences = sent_tokenize(review)
        #for ind, sentence in enumerate(sentences):
        for sentence in sentences:
            for word in suggestive_words:
                if word in sentence.lower().rstrip():
                    corpus_for_string = preprocess_lemm_string(sentence)
                    X_string = token.texts_to_sequences(corpus_for_string)
                    feature = pad_sequences(X_string, 150)
                    output = model.predict(feature)
                    max_ = output[0][0]
                    for j in range(2):
                        if output[0][j]>=max_:
                            max_ = output[0][j]
                            rating = j+1
                    if rating==2:
                        if " it " in sentence or " it's " in sentence or "this" in sentence:
                            try:
                                #print("Used in", sentences[ind-1], sentence)
                                suggestion.append(sentences[ind-1] +" "+ sentence)
                                entity.append(dataset[entity_label][ind])
                            except:
                                    suggestion.append(sentence)
                                    entity.append(dataset[entity_label][ind])
                        else:
                            suggestion.append(sentence)
                            entity.append(dataset[entity_label][ind])
                            
                        #print("found in ", i)
    
    ent_dict = dict()
    for ind, ent in enumerate(entity):
        if str(ent) in ent_dict:
            ent_dict[str(ent)].append(suggestion[ind]) 
        else:
            ent_dict[str(ent)] = [suggestion[ind]]
            
    json_object = json.dumps(ent_dict)
    
    # Saving the File 
    file_name = re.sub(".json", "", file_name)
    with open("static/DBAlpha/FeedbackDB/Results/"+file_name+"_Suggestions.json", "w") as outfile: 
        outfile.write(json_object) 
    
    if return_type == "json":
        final_json_object = json.loads(json_object)
        return final_json_object
    else:
        return list(set(suggestion))



#suggestion_json = predict_suggestions(file_name = "TD20200502024521.json", return_type = "json")

####  TESTING  #########
"""

import pandas as pd
dataset = pd.read_json("static/DBAlpha/TrainingDB/Files/TD20200423214245.json", lines = True)

# To get a JSON try this (entity wise)
suggestion_json = predict_suggestions(dataset, return_type = "json")

# To get list of suggestions try this (not entity wise)
suggestion_list = predict_suggestions(dataset, return_type = "list")

"""
