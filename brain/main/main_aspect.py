"""
1. Module Name: sent_pred (main.sent_pred)
2. Created on Sat Aug 01 2020
3. Authors: Team Alpha Squad
4. Modification History: Nil
   
5. Synopsis: Module to take reviews of n entity and do aspect based analysis on the provided aspects

6. Functions Supported:
    Objects:
        i. Entity_json(file_name, no_entities_attribute_list)
            i. file_name- Name of file on which aspect analysis is to be done
            ii. no_entities- No. of entities on which aspect analysis is to done
            iii. attribute_list- list of attribute on which aspect analysis is to be done
            
            Output:
                Entity_json.created_json- Json file which contain aspect based analysis    

7. Global variables accessed or modified: N/A
"""

# Importing the important libraries
import pandas as pd
import numpy as np
from nltk import sent_tokenize
from main.resources.progress_bar import printProgressBar
# To allow run from the same directory
from main.hybrid_predict import Hybrid_rate
from aspect_based.filter_aspects import return_all_synonyms
from main.make_n_entites import make_entity_wise_json
import json
import re



# Entity_json(filename = "xyz.json", no_entities = 5, attribute_list = ['', ''], entity_column_name, review_column_name, rating_column_name)
class Entity:
    
    # Constructor to set the values
    def __init__(self, file_name = "Appliances.json", no_entities=5, attribute_list = [], entity_label = 'asin', review_label = 'reviewText', rating_label = 'overall', lang = " ", model_file="TD20200309210544"):
        # Initializing Attributes
        self.lang = lang
        self.model_file = model_file
        # First make a json file with 'n' entities
        print("Making JSON file")
        make_entity_wise_json(file_name, no_entities, entity_label, review_label, rating_label)
        # Set the values of the instance variables

        print("Finding Aspects Dynamically")
        self.attribute_list, self.ratings = self.return_aspects_entity_rating(review_label, no_entities, entity_label)
        if len(attribute_list)!=0:
            if no_entities == -1:
                no_entities = len(set(pd.read_json("main/files/uniform_json.json", lines = True)[entity_label]))
            self.attribute_list = [attribute_list for x in range(no_entities)]
        
        print("Processing, Please wait...")
        #print(self.attribute_list)
        self.entities_map = self.map_entity_sentiment("n_entity.json", self.attribute_list)
        self.final_agg, self.attribute_average = self.reduce_entity_map(self.entities_map, self.attribute_list)
        self.xs = self.reduce_to_json(self.final_agg)
        self.created_json = json.loads(str(self.xs))
        self.save_file(file_name)
        
        
    # Function which return an entity map with mapping of each entity rating with the individual aspect rating
    def map_entity_sentiment(self, file_name, attribute_list):         
        # Get the different elements from the provided file and sent request to the get_sent_ratings() function
        dataset = pd.read_json("main/files/"+file_name, lines = True)
        
        review = dataset['reviewText']
        ent = dataset["e_no"]
        asin = dataset['asin']
        range_ = int(dataset.shape[0])
        review_list = []
        
        # Individual Review Rate and Overall Rate DataFrame
#        df_overall = dataset
#        df_overall['sentiment'] = np.nan
        
        # Taking the hybrid classifier in use
        classifier = Hybrid_rate(lang = self.lang, model_file = self.model_file)
        new_dataset = pd.DataFrame()    
        # Traverse through the dataset
        printProgressBar(0, range_, prefix = 'Rating Aspects:', suffix = 'Complete', length = 50)
        for i in range(0, range_): 
            printProgressBar(i, range_, prefix = 'Rating Aspects:', suffix = 'Complete', length = 50)
            
            # Putting Indivial review rating
#            df_overall['sentiment'][i] = classifier.get_hybrid_rating(str(review[i]))
            
            # List of sentences in each review
            review_list.append(sent_tokenize(str(review[i])))  
            # Find rating for each sentence
            for sent in review_list[i]:
                all_aspects = return_all_synonyms(attribute_list[int(ent[i])])
                for a in range(len(attribute_list[int(ent[i])])):
                    for b in range(len(all_aspects[a])):
                        if all_aspects[a][b] in sent.lower():
                            new_dataset = new_dataset.append({'asin': str(asin[i]), 'attribute': attribute_list[int(ent[i])][a],'rating': str(classifier.get_hybrid_rating(str(sent))), 'asp_no': int(ent[i]), 'overall': int(self.ratings[int(ent[i])])}, ignore_index=True)                       
        return new_dataset
    #, df_overall
        
    def return_aspects_entity_rating(self, review_label, no_entities, entity_label):
        
        dataset = pd.read_json("main/files/n_entity.json", lines = True)
        attribute_list = []
        ratings = []
        for i in range(0,dataset.shape[0]):
            if len(dataset["Asp1"][i]) <= 2 :
                continue
            else:
                ratings.append(dataset["Rating"][i])
                attribute_list.append([dataset["Asp1"][i],dataset["Asp2"][i],dataset["Asp3"][i],dataset["Asp4"][i]])
        
        return attribute_list, ratings
    
    def reduce_entity_map(self, entities_map, attribute_list):
        attribute_average = []
        # Starting from the first element
        before = entities_map['asin'][0]
        # New datafram to store the reduced map
        new_dataset = pd.DataFrame()
        # List that will contain ratings of each attribute in a review
        rating_aggregate = [[] for x in range(len(attribute_list[0]))]
        # Number of rows in the entity map
        row = int(entities_map.shape[0])
        # Traverse through each row
        for i in range(0, row):
            after = entities_map['asin'][i]
            
            # If the element is same as before add its atribute rating to the aggregate
            if before != after:
                asp_list = attribute_list[int(entities_map['asp_no'][i-1])]
                total_rat = 0
                total_att = 0
                rating = entities_map['overall'][i]
                # Traverse through the attribute list
                for j in range(0, len(asp_list)):           
                    # If there is no occurance of the attribute then put 0 rating
                    if len(rating_aggregate[j])==0:
                        rating_aggregate[j].append(-1)
                    
                    # Find average rating of that attribute and save it in final rating
                    final_rating = np.average(rating_aggregate[j])   
                    if final_rating!=-1:
                        total_rat += final_rating
                        total_att+=1
                    # Write the values to the new dataset 
                    new_dataset = new_dataset.append({'asin': str(before), 'attribute': asp_list[j],'rating': final_rating},ignore_index=True)         
                total_rat = total_rat/total_att
                # Make the aggrege list ready for next iteration
                rating_aggregate = [[] for x in range(len(attribute_list[0]))]
                attribute_average.append(total_rat)
            try:
                asp_list = attribute_list[int(entities_map['asp_no'][i])]
                # Find the index of the occuring attribute 
                index_ = asp_list.index(str(entities_map['attribute'][i]))                
                # Add the rating of that attribute at its position
                rating_aggregate[index_].append(int(entities_map['rating'][i]))
            except:
                pass
            
            #If it is last iteration, aggregrate it and get out of the loop
            if i==row-1:
                total_rat = 0
                total_att = 0
                asp_list = attribute_list[int(entities_map['asp_no'][i-1])]
                for j in range(0, len(asp_list)):
                    
                    # If there is no occurance of the attribute then put 0 rating
                    if len(rating_aggregate[j])==0:
                        rating_aggregate[j].append(-1)        
                    # Find average rating of that attribute and save it in final rating
                    final_rating = np.average(rating_aggregate[j]) 
                    if final_rating!=-1:
                        total_rat += final_rating
                        total_att+=1
                    # Write the values to the new dataset 
                    new_dataset = new_dataset.append({'asin': str(before), 'attribute': asp_list[j],'rating': final_rating},ignore_index=True)
                total_rat = total_rat/total_att
                attribute_average.append(total_rat)
            
            before = after
        return new_dataset, attribute_average
        
    
    
    # Method to return a json string 
    def reduce_to_json(self,final_agg):     
        # Fist lets take an json string
        json_string = '{"data":['
        # Calculate the total rows in the dataframe
        row = int(final_agg.shape[0])
        before = final_agg['asin'][0]
        # To consider the very first entry in aspects of entities
        count = 0
        flag = 1
        for i in range(0, row):
            # Traverse through each entity
            after = final_agg['asin'][i]
            if before!=after:
                # If some new entity comes close the brackets
                json_string = json_string[:-1]
                json_string = json_string+']},'
                # To indicate first entry in the aspects, make flag=1
                flag = 1
            if flag == 1:
                # If some new entity comes 
                json_string = json_string+ '{"entity":"'+str(after)+'", "overall":"'+str(self.ratings[count])+ '","aspect_avg":"'+ str(self.attribute_average[count])+'", "aspects":['
                count+=1
            # Add the aspect ratings if the rating was not empty(-1)
            if(final_agg['rating'][i]!=-1):
                json_string = json_string+'{"name":"'+str(final_agg['attribute'][i])+'","sentiment":"'+str(final_agg['rating'][i])+'"},'
            # For indicating non-first entry in aspects make flag=0
            flag = 0
            before = after
            
        # If the loop is completed then add the closing brakets
        json_string = json_string[:-1]
        json_string = json_string+']}]}'
        return json_string
    
    def save_file(self, file_name):
        file_name = re.sub(".json", "", file_name)
        self.final_agg.to_csv(r'static/DBAlpha/FeedbackDB/Results/'+file_name+"_Aspect_Based_Analysis.csv", index = True)
        self.final_agg.to_excel(r'static/DBAlpha/FeedbackDB/Results/'+file_name+"_Aspect_Based_Analysis.xlsx", index = True)
#        self.df_overall.to_csv(r'static/DBAlpha/FeedbackDB/Results/'+file_name+"_Overall_Sentiment.csv", index = True)
#        self.df_overall.to_excel(r'static/DBAlpha/FeedbackDB/Results/'+file_name+"_Overall_Sentiment.xlsx", index = True)

#e = Entity(file_name="TD20200323122540.json", no_entities = 10)
#e = Entity(file_name="TD20200502024521.json")
#a = e.attribute_list
#b = e.ratings
#c = e.entities_map
#d = e.final_agg
#f = e.attribute_average
#g = e.xs
#h = e.created_json
#e.save_file(file_name="TD20200502024521.json")
#e.df_overall['sentiment'].mean()
#js = pd.read_json("main/files/n_entity.json", lines = True)
