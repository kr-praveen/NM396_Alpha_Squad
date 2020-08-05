
"""
Desc   : It takes a review json file and return balance reveiw json file (means equal number of each review)

functions : make_balance_json(old_file_name, new_file_name , number of each rating )
                makes new json file with name new_file_name with equal number of each review
                
1. Module Name: make_json (main.make_json)
2. Created on Sat Aug 01 2020
3. Author(s): Team Alpha Squad
  
4. Modification History: NIL
    
5. Synopsis: The make balanced json file with uniform rating distribution

6. Functions Supported:
    a. make_balance_json(file_name, column_review, column_rating, new_file_name, range_of):
        Input Parameters:
            i. filename- filename of dataset (e.g., Appliances.json) stored in location "main/files/"
            ii. column_review- Name of column that contains review strings
            iii. column_rating- Name of the column that contains review for the rating
            iv. new_file_name- Name of new file (with location) where the result is to be written, e.g. files/uniform_json.json
            v. range_of- Number of occurances of reviews with similar ratings in output json file
        Output Parameters:
            Writes the resultant output file in given location

7. Global variables accessed or modified: N/A
"""

import pandas as pd
from main.resources.progress_bar import printProgressBar
def make_balance_json(file_name, column_review, column_rating, new_file_name, range_of):
    dataset = pd.read_json(file_name,lines=True)
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0
    new_dataset = pd.DataFrame()
    
    dataset = dataset.sample(frac=1).reset_index(drop=True)
    
    # Starting progressbar
    printProgressBar(0, range_of*5, prefix = 'Making Json:', suffix = 'Complete', length = 50)
    
    for ind in dataset.index:
        if dataset['overall'][ind]==1 and count_1<range_of:
            new_dataset = new_dataset.append({'review': dataset[column_review][ind], 'rating': dataset[column_rating][ind]},ignore_index=True)
            count_1+=1
        if dataset[column_rating][ind]==2 and count_2<range_of:
            new_dataset = new_dataset.append({'review': dataset[column_review][ind], 'rating': dataset[column_rating][ind]},ignore_index=True)
            count_2+=1
        if dataset[column_rating][ind]==3 and count_3<range_of:
            new_dataset = new_dataset.append({'review': dataset[column_review][ind], 'rating': dataset[column_rating][ind]},ignore_index=True)
            count_3+=1
        if dataset[column_rating][ind]==4 and count_4<range_of:
           new_dataset = new_dataset.append({'review': dataset[column_review][ind], 'rating': dataset[column_rating][ind]},ignore_index=True)
           count_4+=1
        if dataset[column_rating][ind]==5 and count_5<range_of:
           new_dataset = new_dataset.append({'review': dataset[column_review][ind], 'rating': dataset[column_rating][ind]},ignore_index=True)
           count_5+=1
        total_count = count_1 + count_2 + count_3 + count_4 + count_5 
        printProgressBar(total_count, range_of*5, prefix = 'Making Json:', suffix = 'Complete', length = 50)
        if total_count == range_of*5:
            break
    
    new_dataset = new_dataset.sample(frac=1).reset_index(drop=True)
    new_dataset.to_json(new_file_name,orient="records",lines=True)

