"""
Author: Team Alpha Squad
Date  : Sat Aug 01 2020
Desc  : Convert the string to english from any language
func  : convert_to_english(string)
        Input: 
            string : provided string
        Output:
            string in english
"""

from googletrans import Translator
trans = Translator()
def convert_to_english(string):
    
    new_string = trans.translate(string)
    return new_string.text
