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

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Fitting Decision Tree Classification to the Training set
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Applying k-Fold Cross Validation
from performance.kfold import accuracy_score
accuracy_mean, accuracy_std  = accuracy_score(classifier, X_train, y_train, 10)

from performance.kfold import accuracy_macro
precision, recall, fmeasure  = accuracy_macro(classifier, X_train, y_train, 10)