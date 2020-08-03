"""
1. Module Name: model_suggestion
2. Created on Mon Aug 03 2020
3. Author: Team Alpha Squad

4. Modification History:
    NIL
    
5. Synopsis: This module can be used to make a "suggestive model" to find suggestions in a given text

6. Functions Supported:
    a. make_suggestion_model()
        i. Input : 
            i.   Dataset to train,
            ii.  Text Label name
            iii. Output Label name
            
        ii. Operation: make two model
            a. Suggestion model : model to predict suggestion
            b. Token for model  : model to transfor a string according to the model
        
7. Global variables accessed or modified: N/A
"""

# Importing Libraries
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
import pickle
from preprocessings.basic import preprocess_lemm_dataset
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split




def make_suggestion_model(dataset, review_label = 'review', output_label = 'label'):
    corpus = preprocess_lemm_dataset(dataset, review_label)
    y = dataset[output_label]
    TRAINING_VOCAB = 4000
    # Tokenizing the words upto the maximum vocabulary
    tokenizer = Tokenizer(num_words=TRAINING_VOCAB, lower=True, char_level=False)
    # Fitting the corpus to tokenizer
    tokenizer.fit_on_texts(corpus)
    training_sequences = tokenizer.texts_to_sequences(corpus)
    # Getting the encoding dictionary
    vocab_to_int = tokenizer.word_index
    
    sequence_length = 150
    
    # Padding to maximum sequence length
    features = pad_sequences(training_sequences, maxlen = sequence_length)
    
    # Variables for RNN LSTM
    vocab_size = len(vocab_to_int)
    embedding_dim = 256        

    
    # Training parameters
    #batch_size = int(vocab_size//120)
    batch_size = 100
    num_epochs = 30



    # Encoding y data into diffeerent categorical columns
    labelencoder_y = LabelEncoder()
    y = labelencoder_y.fit_transform(y)
    y = y.reshape(len(y),1)
    onehotencoder = OneHotEncoder()
    y = onehotencoder.fit_transform(y).toarray()

    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(features, y, test_size = 0.20, random_state = 0)
    model = Sequential()
    
    # Adding Layers to RNN
    #model.add(Embedding(vocab_size, embedding_dim, weights = [train_embedding_weights],input_length=sequence_length))

    model.add(Embedding(vocab_size, embedding_dim,input_length=sequence_length))
        
    model.add(LSTM(100, return_sequences=True))
    model.add(Dropout(0.4))
    model.add(LSTM(100))
    model.add(Dropout(0.4))
    model.add(Dense(units = 100, kernel_initializer = 'uniform', activation = 'relu'))

    model.add(Dense(2, activation='sigmoid'))
    #rmsprop=optimizers.rmsprop(lr=0.01)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    # Fitting the ANN to the Training set
    model.fit(X_train, y_train, batch_size = batch_size, epochs = num_epochs)
    
    # Predicting the Test set results over trained model
    y_pred = model.predict(X_test)

    # Getting result in proper format that is initially probabilistic
    for i in range(len(y_pred)):
        ind_ = 0
        max_ = y_pred[i][0]
        for j in range(2):
            if y_pred[i][j]>max_:
                max_= y_pred[i][j]
                ind_ = j
            y_pred[i][j]=0
        y_pred[i][ind_]= 1

    y_pred= onehotencoder.inverse_transform(y_pred)
    y_test = onehotencoder.inverse_transform(y_test)
    
    model.save(r'static/DBAlpha/TrainingDB/Models/suggestion.h5')    

    with open(r'static/DBAlpha/TrainingDB/Models/suggestion_token.pkl' , 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
"""
#To create the suggestive model (One time)

import pandas as pd

# Importing Dataset
dataset = pd.read_csv("main/resources/Training2.csv")
dataset = dataset.iloc[:,1:]       
make_suggestion_model(dataset)

"""