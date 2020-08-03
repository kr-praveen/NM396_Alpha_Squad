# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 2020
@author: Team ALpha Squad
"""
import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def analyze_tone(review):    

    authenticator = IAMAuthenticator('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    tone_analyzer = ToneAnalyzerV3(
        version='YYYY-MM-DD',
        authenticator=authenticator
    )
    
    tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/dc6cac79-XXXX-XXXX-XXXX-XXXXXXXXXXXX')

    
    tone_analysis = tone_analyzer.tone(
        {'text': review},
        content_type='application/json'
    ).get_result()
    
    return tone_analysis
