# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 2020

@author: Team Alpha Squad
"""
import numpy as np
import pandas as pd
import json
import re

def progress_timeline(sentiment_rated_json_file):
    df1 = pd.read_json(r'static/DBAlpha/FeedbackDB/Results/'+sentiment_rated_json_file, lines = True)
    
    len_df = df1.shape[0]
    for i in range(len_df):
        df1['reviewTime'][i] = df1['reviewTime'][i][-4:]
    
    df1.sort_values(["asin", "reviewTime"], axis = 0, ascending = (True, True), inplace = True, na_position ='last')
    #df1.reset_index(inplace = True)
    #df1.drop(columns=['index'], inplace = True)
    df1.reset_index(drop = True, inplace = True)
    
    column_names = ["asin", "year", "sentiment"]
    df_pt = pd.DataFrame(columns = column_names)
    
    e_before = df1['asin'][0]
    y_before = df1['reviewTime'][0]
    temp_sum = []
    for i in range(len_df):
        e_after = df1['asin'][i]
        y_after = df1['reviewTime'][i]
        sentiment = df1['sentiment'][i]
        if e_before!=e_after:
            df_pt = df_pt.append({'asin': e_before, 'year': y_before, 'sentiment': np.average(temp_sum)}, ignore_index=True)
            temp_sum = [sentiment]
        elif y_before != y_after:
            df_pt = df_pt.append({'asin': e_before, 'year': y_before, 'sentiment': np.average(temp_sum)}, ignore_index=True)
            temp_sum = [sentiment]
        else:
            temp_sum.append(sentiment)
        if i==len_df-1:
            df_pt = df_pt.append({'asin': e_after, 'year': y_after, 'sentiment': np.average(temp_sum)}, ignore_index=True)
        e_before = e_after
        y_before = y_after
    
    # Saving the Progress Timeline Results
    file_name = re.sub(".json", "", sentiment_rated_json_file)
    df_pt.to_csv(r'static/DBAlpha/FeedbackDB/Results/'+file_name+"_Progress_Timeline.csv", index = True)
    df_pt.to_excel(r'static/DBAlpha/FeedbackDB/Results/'+file_name+"_Progress_Timeline.xlsx", index = True)
    
    
    # Making JSON Object     
    # Fist lets take an json string
    json_string = '{"data":['
    # Calculate the total rows in the dataframe
    row = int(df_pt.shape[0])
    before = df_pt['asin'][0]
    # To consider the very first entry in aspects of entities
    count = 0
    flag = 1
    for i in range(0, row):
        # Traverse through each entity
        after = df_pt['asin'][i]
        if before!=after:
            # If some new entity comes close the brackets
            json_string = json_string[:-1]
            json_string = json_string+']},'
            # To indicate first entry in the aspects, make flag=1
            flag = 1
        if flag == 1:
            # If some new entity comes 
            json_string = json_string+ '{"entity":"'+str(after)+'", "progress":['
            count+=1
            flag = 0
        # Add the aspect ratings if the rating was not empty(-1)
        #if(final_agg['rating'][i]!=-1):
        json_string = json_string+'{"year":"'+str(df_pt['year'][i])+'","sentiment":"'+str(df_pt['sentiment'][i])+'"},'
        # For indicating non-first entry in aspects make flag=0
        before = after
        
    # If the loop is completed then add the closing brakets
    json_string = json_string[:-1]
    json_string = json_string+']}]}'
    json_ob = json.loads(json_string)
    return json_ob