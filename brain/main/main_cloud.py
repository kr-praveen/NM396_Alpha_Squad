# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 2020

@author: Team Alpha Squad
"""

import boto3


# Inserting in Database
dynamoDB = boto3.resource('dynamodb')
dynamoTable = dynamoDB.Table('feedback-form-data')

def get_file_name_by_id(id):
    response = dynamoTable.get_item(
        Key={
            'date': id
        }
    )
    item = response['Item']
    return item['fd_file']
