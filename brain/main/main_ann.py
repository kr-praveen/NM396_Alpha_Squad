"""
1. Module Name: main_ann (main.main_ann)
2. Created on Sat Aug 01 2020
3. Authors: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 2020
    
       
5. Synopsis: The main module to run the ANN classifier

6. Functions Supported:
    a. make_model(file_name, column_review, column_rating, json_balanced=False, have_corpus=False, size=5000, cv_vectors = 3000):
        Input Parameters:
            i. filename- filename of dataset (e.g., Appliances.json) stored in location "main/files/"
            ii. column_review- Name of column that contains review strings
            iii. column_rating- Name of the column that contains review for the rating
            iv. json_balanced (default: False)- Is relevant uniform json file (uniform_json.json) already present in location "main/files/" 
            v. have_corpus (default: False)- Is relevant corpus file (corpus.txt) already present in "main/resources"
            vi. size (default: 5000)- Size of dataset to be processed
            vii. cv_vectors (default: 3000)- Number of maximum features to be considered during Count Vectorization
        Output Parameters:
            Saves prepared ANN model trained over 5 categories (5 classes) in "main/models" directory as "model.pkl" file.
            i. accuracy- Accuracy of model over testing data
            ii. precision- Precision of model over testing data
            iii. recall- Recall of model over testing data
            iv. fmeasure- F-measure of model over testing data 

7. Global variables accessed or modified: N/A

"""

from pandas import read_json
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import accuracy_score
from make_json import make_balance_json
import sys
sys.path.append("../")
from bagging import bagging_x
from preprocessings import basic, process_corpus
from performance.accuracy_measures import accuracy_macro
import pickle
from sklearn.metrics import confusion_matrix

# Definition of make_model() function
def make_model(file_name, column_review, column_rating, json_balanced=False, have_corpus=False, size=5000, cv_vectors = 3000):
    
    # Making a json file with balanced ratings
    if json_balanced == False:
        make_balance_json("files/"+file_name, column_review, column_rating,"files/uniform_json.json",size/5)
    dataset = read_json('files/uniform_json.json', lines= True)
    
    # Making corpus, in case corpus doesn't exists
    if have_corpus == False:
        corpus = basic.preprocess_lemm_dataset(dataset,'review')
        process_corpus.write_corpus(corpus)
    
    # If corpus exists, read it directly 
    else:
        corpus =[]
        corpus = process_corpus.read_corpus()
        corpus = corpus[:size] 

    # Performing count vectorization over X
    X = bagging_x.get_X_vector(corpus, cv_vectors)
    y = dataset.iloc[:size, 0]

    # Encoding y data into diffeerent categorical columns
    labelencoder_y = LabelEncoder()
    y = labelencoder_y.fit_transform(y)
    y = y.reshape(len(y),1)
    onehotencoder = OneHotEncoder(categorical_features = [0])
    y = onehotencoder.fit_transform(y).toarray()

    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
    
    # Initialising the ANN
    classifier = Sequential()
    
    # Adding the input layer and the first hidden layer
    classifier.add(Dense(units = int(cv_vectors/4), kernel_initializer = 'uniform', activation = 'relu', input_dim = cv_vectors))
    
    # Adding the second and third hidden layers
    classifier.add(Dense(units = int(cv_vectors/4), kernel_initializer = 'uniform', activation = 'relu'))
    classifier.add(Dense(units = int(cv_vectors/4), kernel_initializer = 'uniform', activation = 'relu'))
    
    # Adding the output layer
    classifier.add(Dense(units = 5, kernel_initializer = 'uniform', activation = 'sigmoid'))
    
    # Compiling the ANN
    classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    
    # Fitting the ANN to the Training set
    classifier.fit(X_train, y_train, batch_size = 150, nb_epoch = 30)
    
    # Predicting the Test set results over trained model
    y_pred = classifier.predict(X_test)
    
    # Getting result in proper format that is initially probabilistic
    for i in range(len(y_pred)):
        ind_ = 0
        max_ = y_pred[i][0]
        for j in range(5):
            if y_pred[i][j]>max_:
                max_= y_pred[i][j]
                ind_ = j
            y_pred[i][j]=0
        y_pred[i][ind_]= 1
    
    # Inverse Transforming the categorical encodings on y_pred and y_test
    y_pred= onehotencoder.inverse_transform(y_pred)
    y_test = onehotencoder.inverse_transform(y_test)
    
    # Measuring the performance
    accuracy = accuracy_score(y_test,y_pred,normalize=True, sample_weight=None)
    precision, recall, fmeasure = accuracy_macro(y_test, y_pred)

    # Saving the model
    pickle.dump(classifier, open('models\model.pkl','wb'))
    
    cm = confusion_matrix(y_test, y_pred)
    
    # Returning the performance parameters
    return accuracy,precision,recall, fmeasure, cm
