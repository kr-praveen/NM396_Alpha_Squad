# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 2020

@author: Team Alpha Squad
"""

import json


IBM_WATSON_NLU_API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
IBM_WATSON_NLU_VERSION = 'YYYY-MM-DD'
IBM_WATSON_NLU_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def extract_entities(review):
    from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions
    
    authenticator = IAMAuthenticator(IBM_WATSON_NLU_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version=IBM_WATSON_NLU_VERSION,
        authenticator=authenticator
    )
    
    natural_language_understanding.set_service_url(IBM_WATSON_NLU_URL)
    
    response = natural_language_understanding.analyze(
    text=review,
    features=Features(entities=EntitiesOptions(sentiment=True, limit=2))).get_result()
    
    return response
