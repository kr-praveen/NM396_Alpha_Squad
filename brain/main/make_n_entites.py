"""
1. Module Name: make_n_entities (main.make_n_entities)
2. Created on Sat Aug 01 2020
3. Author: Team Alpha Squad
4. Modification History: Nil

    
5. Synopsis: Module to find out 'n' number of entity's review from the review set

6. Functions Supported:
    a. make_entity_wise_json(file_name, no_entities)
        Input Parameters:
            i.   file_name- Name of the file to which we need to take out entities
            ii.  no_entites- Total number of entity to consider
            iii. entity_label- label name of the column with entities
            iv.  review_label- label name of the column with reviews
            v.   rating_label- label name of the column with ratings 

7. Global variables accessed or modified: N/A

"""

import pandas as pd
import sys
sys.path.append("../")
from aspect_based.filter_aspects import Attributes
from main.hybrid_predict import Hybrid_rate
import numpy as np
from main.resources.progress_bar import printProgressBar

model = Hybrid_rate()

def make_entity_wise_json(file_name, no_entities, entity_label='asin', review_label='reviewText', rating_label='overall'):
    # To get dataset from same directory i.e. inside main as well as from the app i.e. outside main
    dataset = pd.read_json("static/DBAlpha/FeedbackDB/Files/"+file_name, lines = True)
        
    # Sort the dataset and order by entity so that same entity can be together (Used to seperate them)
    dataset = dataset.sort_values(by = entity_label)
    dataset = dataset.reset_index(drop = True)
    
    # Initializing values to empty
    dataset["Asp1"] = ""
    dataset["Asp2"] = ""
    dataset["Asp3"] = ""
    dataset["Asp4"] = ""
    dataset["Asp5"] = ""
    dataset["Rating"] = 0
    dataset["e_no"] = 0
    

    
    # Before and after variables would be used to see a change in the entity id
    before = dataset[entity_label][0]
    
    # Counter to cout number of entities
    count = 0
    rating = []
    review_text = ""
    # Traverse through the rows of the dataset
    printProgressBar(0, no_entities, prefix = 'Making Json:', suffix = 'Complete', length = 50)
    
    for i in range(0,dataset.shape[0]):
        after = dataset[entity_label][i]
        
        # If new entity comes increase the counter
        if after!=before:
            av_rating = np.average(rating)
            asp_obj = Attributes([review_text])
            asp_list = asp_obj.filtered_attributes
            for j in range(5):
                dataset.iloc[i-1, dataset.columns.get_loc("Asp"+str(j+1))] = asp_list[j]
            
            dataset.iloc[i-1, dataset.columns.get_loc("Rating")] = av_rating
            review_text = ""
            review_text = review_text + str(dataset[review_label][i])
            count += 1
            rating = []
            
        else:
            review_text = review_text + str(dataset[review_label][i])
        
        cur_rat = model.get_hybrid_rating(str(dataset.iloc[i, dataset.columns.get_loc(review_label)]))
        rating.append(cur_rat)
            
        before = after
        
        dataset.iloc[i, dataset.columns.get_loc("e_no")] = count
        
        # If we get the requiered amount of quantities break the loop
        if count == no_entities:
            dataset = dataset[0:i]
            break
        
        # If it is the last entry, then aggregrate for this entiy also
        if i==(dataset.shape[0]-1):
            av_rating = np.average(rating)
            asp_obj = Attributes([review_text])
            asp_list = asp_obj.filtered_attributes
            for j in range(5):
                dataset.iloc[i-1, dataset.columns.get_loc("Asp"+str(j+1))] = asp_list[j]
            
            dataset.iloc[i-1, dataset.columns.get_loc("Rating")] = av_rating
            review_text = ""
            review_text = review_text + str(dataset[review_label][i])
            count += 1
            rating = []
        
        printProgressBar(count, no_entities, prefix = 'Making Json:', suffix = 'Complete', length = 50)
        
    # Writing the new dataset to file named : n_entity.json
    try:
        dataset.to_json('main/files/'+"n_entity.json", orient="records", lines=True)
    except:
        dataset.to_json('files/'+"n_entity.json", orient="records", lines=True)
