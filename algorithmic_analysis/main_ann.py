# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_json('Dataset_50000.json', orient = 'columns', lines = True)

# Basic Pre-processing using preprocessing.basic modal
from preprocessing.basic import preprocess_feedbacks
corpus = preprocess_feedbacks(dataset, 'reviewText')

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 15000)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 0].values

# Encoding y data into diffeerent categorical columns
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)
y = y.reshape(len(y),1)
onehotencoder = OneHotEncoder(categorical_features = [0])
y = onehotencoder.fit_transform(y).toarray()

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense

# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(output_dim = 2000, init = 'uniform', activation = 'relu', input_dim = 4000))

# Adding the second hidden layer
classifier.add(Dense(output_dim = 2000, init = 'uniform', activation = 'relu'))

# Adding the third hidden layer
classifier.add(Dense(output_dim = 2000, init = 'uniform', activation = 'relu'))

# Adding the output layer
classifier.add(Dense(output_dim = 5, init = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
classifier.fit(X_train, y_train, batch_size = 50, nb_epoch = 5)


# Predicting the Test set results
y_pred = classifier.predict(X_test)

for i in range(200):
    for j in range(5):
        y_pred[i][j] = y_pred[i][j]>0.5



y_pred= onehotencoder.inverse_transform(y_pred)
y_test = onehotencoder.inverse_transform(y_test)


# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

from performance.accuracy_measures import accuracy_macro
precision, recall, fmeasure = accuracy_macro(y_test, y_pred)