"""
1. Module Name: main_rnn (main.main_rnn)
2. Created on Sat Aug 01 2020
3. Author: Team Alpha Squad

4. Modification History:
    NIL
      
5. Synopsis: The main module to run the RNN classifier

6. Functions Supported:
    a. make_model(file_name, column_review, column_rating, json_balanced=False, have_corpus=False, size=5000):
        Input Parameters:
            i. filename- filename of dataset (e.g., Appliances.json) stored in location "main/files/"
            ii. column_review- Name of column that contains review strings
            iii. column_rating- Name of the column that contains review for the rating
            iv. json_balanced (default: False)- Is relevant uniform json file (uniform_json.json) already present in location "main/files/" 
            v. have_corpus (default: False)- Is relevant corpus file (corpus.txt) already present in "main/resources"
            vi. size (default: 5000)- Size of dataset to be processed
        Output Parameters:
            Saves prepared ANN model trained over 5 categories (5 classes) in "main/models" directory as "model.pkl" file.
            i. accuracy- Accuracy of model over testing data
            ii. precision- Precision of model over testing data
            iii. recall- Recall of model over testing data
            iv. fmeasure- F-measure of model over testing data 
            v. confusion_matrix
7. Global variables accessed or modified: N/A
"""
from pandas import read_json
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from sklearn.metrics import accuracy_score
from main.make_json import make_balance_json
from preprocessings import basic, process_corpus
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import re
from os import mkdir
#import gensim.models as models

# Running Tensorflow through GPU
try:
    import tensorflow.python.keras.backend as K
    sess = K.get_session()
except:
    print("GPU not found")

# Definition of make_model() function
def make_model(file_name = "TD20200309210544.json", column_review = "reviewText", column_rating = "overall", json_balanced=True, have_corpus=True, size=10000):
    
    # Making a json file with balanced ratings
    if json_balanced == False:
        make_balance_json(r'static/DBAlpha/TrainingDB/Files/'+file_name, column_review, column_rating,"main/files/uniform_json.json",size/5)
    dataset = read_json('main/files/uniform_json.json', lines= True)
    dataset = dataset[:size]

    # Making corpus, in case corpus doesn't exists
    if have_corpus == False:
        corpus = basic.preprocess_lemm_dataset(dataset,'review')
        process_corpus.write_corpus(corpus)
    
    # If corpus exists, read it directly 
    else:
        corpus =[]
        corpus = process_corpus.read_corpus()
        corpus = corpus[:size] 

    # Getting the ratings
    y = dataset.iloc[:size, 0]
    
    # Maximum words to consider
    TRAINING_VOCAB = 5000
    
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
    
    """
    EMBEDDING_DIM = 300
    # Loading google's words to vect embedding
    print("\nLoading the Google's word2vec \nPlease Wait...")
    word2vec_path = 'resources/GoogleNews-vectors-negative300.bin'
    word2vec = models.KeyedVectors.load_word2vec_format(word2vec_path, binary=True)
    
    train_embedding_weights = np.zeros((len(vocab_to_int), EMBEDDING_DIM))
    for word,index in vocab_to_int.items():
        if word in word2vec:
            train_embedding_weights[index,:] = word2vec[word]  
        else:
            np.random.rand(EMBEDDING_DIM)
    print(train_embedding_weights.shape)
    """
    
    # Variables for RNN LSTM
    vocab_size = len(vocab_to_int)
    embedding_dim = 512        

    
    # Training parameters
    batch_size = int(size//100)
    num_epochs = 30



    # Encoding y data into diffeerent categorical columns
    labelencoder_y = LabelEncoder()
    y = labelencoder_y.fit_transform(y)
    y = y.reshape(len(y),1)
    onehotencoder = OneHotEncoder()
    y = onehotencoder.fit_transform(y).toarray()

    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(features, y, test_size = 0.20, random_state = 0)
    
    
    # Initialising the RNN
    model = Sequential()
    
    # Adding Layers to RNN
    #model.add(Embedding(vocab_size, embedding_dim, weights = [train_embedding_weights],input_length=sequence_length))
    if size > 2000:
        model.add(Embedding(TRAINING_VOCAB, embedding_dim,input_length=sequence_length))
    else:
        model.add(Embedding(TRAINING_VOCAB, size/10, input_length=sequence_length))
        
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100))
    model.add(Dense(units = 200, kernel_initializer = 'uniform', activation = 'relu'))

    model.add(Dense(5, activation='sigmoid'))
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
    accuracy = accuracy_score(y_test, y_pred,normalize=True, sample_weight=None)
    
    #
    file_name = re.sub(".json", "", file_name)
    with open(r'static/DBAlpha/TrainingDB/Models/TOKEN_' + file_name + ".pkl" , 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    model.save(r'static/DBAlpha/TrainingDB/Models/'+file_name+'.h5')    
    
#     Returning the performance parameters
    return accuracy
