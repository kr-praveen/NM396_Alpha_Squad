"""
Summary : 
Functions Supported : write_corpus(corpus_name)
                        writes the corpus to the file named "corpus.txt"
                    read_corpus()
                        read copus from the file "corpus.txt"
                        
1. Module Name: process_corpus (preprocessing.process_corpus)
2. Created on Sat Aug 01 11:33:01 2020
3. Author: Team Alpha Squad

4. Modification History:
    1st modification on: Sat Aug 01 11:33:01 2020
	
5. Synopsis: A module to read and write corpus to a .txt file and thus, increasing the performance

6. Functions Supported:
    a. write_corpus(corpus):
        Input Parameters:
            i. corpus- List of pre-processed review strings that is to be stored as .txt file
        Output Parameters:
            Corpus text file is stored as "corpus.txt" at location "main/resources"

    b. read_corpus():
        Output Parameters:
            i. corpus- List with pre-processed review strings as fetched from file "main/resources/corpus.txt"
"""

def write_corpus(corpus):
    with open('resources/corpus.txt', 'w') as filehandle:
        for listitem in corpus:
            filehandle.write('%s\n' % listitem)


def read_corpus():
    corpus = []
    # open file and read the content in a list
    with open('resources/corpus.txt', 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]
    
            # add item to the list
            corpus.append(currentPlace)
    return corpus