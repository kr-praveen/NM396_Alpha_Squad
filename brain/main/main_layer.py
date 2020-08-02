# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 2020

@author: Team Alpha Squad
"""
from main.main_aspect import Entity
from main.main_overall import overall_rate
from main.progress_timeline_analysis import progress_timeline
from suggestion_defect.predict_suggestion import predict_suggestions

def full_analysis(file_name = "TD20200502024521.json", model_file="TD20200309210544", no_entities = 4, lang = ""):
    entity = Entity(file_name = file_name, no_entities = no_entities, model_file = model_file)
    json_obj_aspect_based = entity.created_json
    overall_mean = overall_rate(file_name, lang, model_file)
    json_obj_progress_timeline = progress_timeline(file_name)
    suggestion_json = predict_suggestions(file_name = file_name, return_type = "json")
    return json_obj_aspect_based, overall_mean, json_obj_progress_timeline, suggestion_json
