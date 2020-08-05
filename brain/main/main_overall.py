# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 2020

@author: Team Alpha Squad
"""  

import pandas as pd
import numpy as np
from main.hybrid_predict import Hybrid_rate
import re

def overall_rate(file_name, lang = "", model_file = "TD20200309210544"):
    df = pd.read_json(r'static/DBAlpha/FeedbackDB/Files/'+file_name, lines = True)
    df.sort_values("asin", axis = 0, ascending = True, inplace = True, na_position ='last')
    df.reset_index(drop = True, inplace = True)
    classifier = Hybrid_rate(lang, model_file)
    df['sentiment'] = np.nan
    for i in range(df.shape[0]):
        df['sentiment'][i] = classifier.get_hybrid_rating(df['reviewText'][i])
    df.to_json(r'static/DBAlpha/FeedbackDB/Results/'+file_name, orient = 'records', lines = True)
    file_name = re.sub(".json", "", file_name)
    df.to_csv(r'static/DBAlpha/FeedbackDB/Results/'+file_name+"_Individual_Comment_Ratings.csv", index = True)
    df.to_excel(r'static/DBAlpha/FeedbackDB/Results/'+file_name+"_Individual_Comment_Ratings.xlsx", index = True)
    return df['sentiment'].mean()
