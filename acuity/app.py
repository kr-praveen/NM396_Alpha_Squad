"""
1. Module Name: kfold (performance.kfold)
2. Created on Sat Aug 01 02:33:09 2020
3. Author: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 02:33:09 2020
    
5. Synopsis: Main application file for flask web frameworks

6. Functions Supported:
    a. list_to_string(input_list):
        Input Parameters: list to be converted in string
        Output Parameters: resultant string
    b. home():
        To render main index.html page
    c. predict():
        To render index.html/predict url
        Predicts sentiment over a feedback string
        
"""


# Importing required libraries
from flask import Flask, request, jsonify, render_template
from main.lexical_predict import Lexical_rate

def list_to_string(input_list):
    # initialize an empty string 
    resultant_string = ""  
    # traverse in the string   
    for word in input_list:  
        resultant_string += word
    # return string   
    return resultant_string


# Initializing the flask framework
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    rating = 0
    feedback = [str(x) for x in request.form.values()]
    model = Lexical_rate()
    rating = model.get_rating(list_to_string(feedback))
    return render_template('index.html', predicted_result = rating)
    
    
if __name__ == "__main__":
    app.run(debug=False)