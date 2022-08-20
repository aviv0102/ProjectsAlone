'''
Itay Hassid 209127596   Aviv Shisman 206558157
'''

# imports:
import sys
import numpy as np


'''
Our program checks for words similar to the target words using the word2Vec PreCalculated matrices(G and W, recall when 
we multiply them we get the PMI matrix) this time we use the Word2Vec algorithm and then 
we only need to evaluate results by using the cosine(only dot this time)

input: target words(hardcoded), WPath (arg1) , GPath(arg2)

output: similar words to targets (using the 3 methods) 
'''
def main():
    if len(sys.argv) != 3:
        print('invalid input')
        return

    # W is the reduced matrix of words that word2vec creates from the data
    W = sys.argv[1]
    # G is the reduced matrix of contexts
    G= sys.argv[2]

    params = loadCorpus(W,G)

    compare(params)


'''
Loading Word2Vec precalculated results
'''
def loadCorpus(WPath,GPath):

    print('Loading word2Vec info..')

    targets = ["car", "bus", "hospital", "hotel", "gun", "bomb", "horse", "fox", "table", "bowl", "guitar",
               "piano"]

    #loading the info
    with open(WPath) as vector_file:
        x = len(vector_file.readline().split(' '))

    with open(GPath) as s_file:
        y = len(s_file.readline().split(' '))

    print('Done\n')

    #creating the parameters
    print('Creating Parameters...')
    W = np.loadtxt(WPath, delimiter=' ', usecols=range(1, x))
    G = np.loadtxt(GPath, delimiter=' ', usecols=range(1, y))
    lemmas = np.loadtxt(WPath, delimiter=' ', usecols=[0], dtype=str)
    word_to_index = {word: i for i, word in enumerate(lemmas)}
    att = np.loadtxt(GPath, delimiter=' ', usecols=[0], dtype=str)
    params=Params(W,G,lemmas,word_to_index,att,targets)
    print('Done\n')

    return params


'''
Info class for holding params
'''
class Params:

    def __init__(self,W, G, lems,w2Index,attributes,tar):
        self.W = W
        self.G = G
        self.lemmas = lems
        self.word_to_index = w2Index
        self.att = attributes
        self.targets = tar



'''
Finding all the good comparisons for the target words
'''
def compare(params):

    print('Results:\n\n')
    #get Params
    W=params.W
    G=params.G
    word_to_index=params.word_to_index
    att = params.att
    targets=params.targets
    lemmas=params.lemmas

    #compare by word:
    k=20
    print ('Compare by word:')
    for word in targets:
        print ('\ntarget word: ' + word)
        #get the vector of the word in the matrix
        W_wordIndex = W[word_to_index[word]]

        #get all the words similar to the word by dot product(cosine)
        CosineVal = W.dot(W_wordIndex)

        #print the first 20
        most_similar_idx = (-CosineVal).argsort()
        similar_words = lemmas[most_similar_idx]
        for i in range (k+1):
            print(similar_words[i]+',', end = ' ')

    print ('\n\n')


    print('to attributes(1st order):')
    k=10
    for word in targets:
        print ('\ntarget word: ' + word)

        #get the vector of the word in the matrix
        W_wordIndex = W[word_to_index[word]]

        #get all the words similar to the word by dot product(cosine) but this time by attribute
        CosineVal = G.dot(W_wordIndex)
        most_similar_idx = (-CosineVal).argsort()
        similar_words = att[most_similar_idx]
        for i in range (k+1):
            print(similar_words[i]+',', end = ' ')






if __name__ == '__main__':
    main()


