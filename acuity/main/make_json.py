"""              
1. Module Name: make_json (main.make_json)
2. Created on Sat Aug 01 12:40:29 2020
3. Author: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 12:40:29 2020
    
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
def make_balance_json(file_name, column_review, column_rating, new_file_name, range_of):
    dataset = pd.read_json(file_name,lines=True)
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0
    new_dataset = pd.DataFrame()
    
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
        
    new_dataset.to_json(new_file_name,orient="records",lines=True)

