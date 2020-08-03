# -*- coding: utf-8 -*-
"""

Created on Mon Aug 03 2020

@author: Team Alpha Squad
"""
import boto3
import pandas as pd

def store_web_api():
    dynamoDB = boto3.resource('dynamodb')
    dynamoTable = dynamoDB.Table('feedback')
    response = dynamoTable.scan()
    items = response['Items']
    df = pd.DataFrame(items)
    df.to_json(r"static/DBAlpha/FeedbackDB/Files/WebAPI.json", orient = 'records', lines = True)