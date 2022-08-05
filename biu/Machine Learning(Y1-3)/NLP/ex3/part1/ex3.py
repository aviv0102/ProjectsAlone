'''
Itay Hassid 209127596   Aviv Shisman 206558157
'''

# imports:
import sys
import math
import numpy as np


'''
Our program checks for words similar to the target words using the corpus it gets,
we use the algorithm we learned in lecture 6 to turn each word to PMI vector that represent its meaning
and then use cosine to compare it to other words.

input: target words(hardcoded), corpus (arg1)
output: similar words to targets (using the 3 methods) 
'''
def main():
    if len(sys.argv) != 2:
        print('invalid input')
        return
    filename = sys.argv[1]
    print('Start Loading Data...')
    print('Please hold on for a few seconds\n\n')
    params = loadCorpus(filename)
    results(params)


'''
Loading Corpus to memory, Extracting parameters
'''
def loadCorpus(filename):
    print('Reading Corpus...')

    # Open the corpus and getting the required params from it
    corpus = []
    f = open(filename)
    sentence = []
    for line in f.readlines():
        word = line.split()
        if len(word) == 0:
            corpus.append(sentence)
            sentence = []
        else:
            sentence.append((word[2], word[3], word[6]))
    f.close()
    print('Done\n')
    return extractParams(corpus)

'''
Extracting the parameters 
'''
def extractParams(corpus):


    # All the words in vocabularery
    print ('Extracting Parameters...')

    lemma = [word for sentence in corpus for word, y, z in sentence]
    lemmas = set(lemma)

    # Convert word to index and then update global param
    w2v = {w: i for i, w in enumerate(lemmas)}

    # Convert index to word and update the global param
    v2w = {i: w for i, w in enumerate(lemmas)}

    # Counting all words in vocabulary
    num_of_lemmas = {}
    for lem in lemma:
        elm = w2v[lem]
        if elm not in num_of_lemmas.keys():
            num_of_lemmas[elm] = 1
        else:
            num_of_lemmas[elm] += 1

    #the words we want to find similarities for
    target_words = ["car", "bus", "hospital", "hotel", "gun", "bomb", "horse", "fox", "table", "bowl", "guitar",
                    "piano"]
    target_Idx = [w2v[word] for word in target_words]

    params = CorpusParams(corpus, lemmas, w2v, v2w, num_of_lemmas, target_Idx)

    print('Done\n')

    return params

    # for checking later


'''
Info class for holding params
'''
class CorpusParams:

    def __init__(self, cor, lems, w2v, v2w, lemCounter,tagIdx):
        self.corpus = cor
        self.lemmas = lems
        self.word_to_vector = w2v
        self.vector_to_word = v2w
        self.lemmas_count = lemCounter
        self.tagIdx=tagIdx


'''
First Method, Calc by sentence
'''
def calcBySentence(params):

    print ("Counting by all the words in the sentence method (please wait a few moments)")
    # Getting params:
    corpus = params.corpus
    word_to_vector = params.word_to_vector
    num_of_lemmas = params.lemmas_count

    # Counting (u,att)
    CountDict = {}

    # Dict for each att, what words it paired with(for later calculations)
    attMap = {}

    # Trasholds
    MinWordCount = 100
    MinAttCount = 30


    #filter unuseful words that occur often
    filter_words = ['(', ')', ',', '.', 'DT', 'IN', 'TO', 'RP', 'POS', 'PRP', 'PRP$', 'MD', 'CC', 'WDT', 'PDT']

    num=0

    # Main loop:
    for sentence in corpus:

        #filter the unInformative words
        filteredSentence = [word for word, t, _ in sentence if t not in filter_words]

        for word in filteredSentence:
            IndexOfWord = word_to_vector[word]

            # Only words that occur more then 100 times in lemma form
            if num_of_lemmas[IndexOfWord] < MinWordCount:
                continue
            else:
                # In case the index of word not in countDict create its dictionary of attributes
                if IndexOfWord not in CountDict:
                    CountDict[IndexOfWord] = {}

                # Going through all the other words in the sentence and counting the combination of them with 'Word'
                for secondWord in filteredSentence:
                    if word != secondWord:
                        att = secondWord
                        attIdx = word_to_vector[att]

                        # Only att with more than 20 appearances
                        if num_of_lemmas[attIdx] > MinAttCount:
                            num+=1

                            # Counting (word,att)
                            if attIdx not in CountDict[IndexOfWord]:
                                CountDict[IndexOfWord][attIdx] = 1
                            else:
                                CountDict[IndexOfWord][attIdx] += 1

                            # for each att, we have a set of all the words it was paired with
                            if attIdx not in attMap:
                                attMap[attIdx] = set()
                            else:
                                attMap[attIdx].add(IndexOfWord)
    print ("Done\n")

    print(num)

    return CountDict, attMap

'''
second method - calc by window
'''
def calcByWindow(params):

    print ("Counting by a window method(please wait a few moments)")

    minimum_word_occurance = 100
    minimum_feature_occurance = 30
    table = {}  #words table
    attribute_map = {}
    filter_words = ['(', ')', ',', '.', 'DT', 'IN', 'TO', 'RP', 'POS', 'PRP', 'PRP$', 'MD', 'CC', 'WDT', 'PDT']

    #get Params
    corpus = params.corpus
    word_to_vector = params.word_to_vector
    num_of_lemmas = params.lemmas_count


    for sentence in corpus:
        filtered = [word for word, t, _ in sentence if t not in filter_words]
        for i, word in enumerate(filtered):
            index = word_to_vector[word]
            if num_of_lemmas[index] < minimum_word_occurance:
                continue
            if index not in table.keys():
                table[index] = {}
            for j in [-2, -1, 1, 2]:
                if (i + j < 0) or (i + j >= len(filtered)):
                    continue
                att_index = word_to_vector[filtered[i + j]]
                if num_of_lemmas[att_index] < minimum_feature_occurance:
                    continue

                if att_index not in table[index].keys():
                    table[index][att_index] = 1
                else:
                    table[index][att_index] += 1
                if att_index not in attribute_map.keys():
                    attribute_map[att_index] = set()
                attribute_map[att_index].add(index)
    print('Done\n')
    return table, attribute_map



'''
third method - calc by the dependency
'''
def calcByDependency(params):
    print("Counting by a dependency method(please wait a few moments)")
    minimum_word_occurance = 100
    minimum_feature_occurance =30
    table = {}  # words table
    attribute_map = {}
    filter_words = ['(', ')', ',', '.', 'DT', 'IN', 'TO', 'RP', 'POS', 'PRP', 'PRP$', 'MD', 'CC', 'WDT', 'PDT']
    # get Params
    corpus = params.corpus
    word_to_vector = params.word_to_vector
    num_of_lemmas = params.lemmas_count

    for sentence in corpus:
        for word, tag, head in sentence:
            if tag in filter_words:
                continue
            index = word_to_vector[word]
            # not enough occurances of this word
            if num_of_lemmas[index] < minimum_word_occurance:
                continue
            if index not in table.keys():
                table[index] = {}
            next_word = sentence[int(head) - 1]
            if next_word[1] == 'IN':
                next_next_word_idx = int(next_word[2]) - 1
                attr_index = word_to_vector[sentence[next_next_word_idx][0]]
                attr_tag = sentence[next_next_word_idx][1]
                direction = 'up'
            else:
                attr_index = word_to_vector[next_word[0]]
                attr_tag = next_word[1]
                direction = 'down'
            # put dependency edge
            if num_of_lemmas[attr_index] >= minimum_feature_occurance:
                if (attr_index, attr_tag, direction) not in table[index].keys():
                    table[index][(attr_index, attr_tag, direction)] = 1
                else:
                    table[index][(attr_index, attr_tag, direction)] += 1
                if (attr_index, attr_tag, direction) not in attribute_map:
                    attribute_map[(attr_index, attr_tag, direction)] = set()
                attribute_map[(attr_index, attr_tag, direction)].add(index)
            # put counter dependency edge
            if num_of_lemmas[attr_index] < minimum_word_occurance:
                continue
            if attr_index not in table.keys():
                table[attr_index] = {}
            if num_of_lemmas[attr_index] >= minimum_feature_occurance:
                direction = 'up' if (direction == 'down') else 'up'
                if (attr_index, attr_tag, direction) not in table[index].keys():
                    table[index][(attr_index, attr_tag, direction)] = 1
                else:
                    table[index][(attr_index, attr_tag, direction)] += 1
                if (attr_index, attr_tag, direction) not in attribute_map:
                    attribute_map[(attr_index, attr_tag, direction)] = set()
                attribute_map[(attr_index, attr_tag, direction)].add(index)
    print('Done\n')
    return table, attribute_map

'''
get results
'''
def results(params):

    CountDict2,AttMap2 = calcByWindow(params)
    compare(params,AttMap2,CountDict2)

    CountDict, AttMap = calcByDependency(params)
    compare(params,AttMap,CountDict)

    CountDict3,AttMap3 = calcBySentence(params)
    compare(params,AttMap3,CountDict3)


'''
Calc the vector of PMI values of each word (in the lecture we saw as word count instead of pmi values)
'''
def CalcWordVecPMI(countDict):

    print ('Create PMI Vectors Starting...')

    # getting sum and count of all pairs for PMI
    numAllPairs=0
    sumAllPairs=0
    for wordIdx in countDict:
        for attIdx in countDict[wordIdx]:
            numAllPairs+=1
            sumAllPairs+=countDict[wordIdx][attIdx]

    # declare vars:
    word_count = {}
    att_count = {}
    word_att_appearances_count = {}
    Word_PMIVec = {}

    # calc each appearances:
    for word in countDict:

        #the dict in entery word=> its keys are the attributes of word
        wordDict=countDict[word]

        # count the number of time word='theCurrWord' appears
        if word not in word_count:
            word_count[word] = 0

        # check if 'word' is in the combination dict if not open a entry for it(each word has its own dict)
        if word not in word_att_appearances_count:
            word_att_appearances_count[word] = {}

        # adding the count...
        for attr in wordDict:
            CurrentValue=float(countDict[word][attr])
            if attr not in att_count:
                att_count[attr] = 0
            att_count[attr] += CurrentValue
            word_count[word] += CurrentValue
            word_att_appearances_count[word][attr] =CurrentValue

    for word in countDict:
        # creating a pmi vector for each word(to later use cosine on)
        if word not in Word_PMIVec:
            Word_PMIVec[word] = {}

        #calculating pmi for each att in the vector like we learned in lecture
        for attr in countDict[word]:
            Word_PMIVec[word][attr] = max(math.log(((word_att_appearances_count[word][attr] * sumAllPairs) /
                                                    ((word_count[word]**0.75) * att_count[attr])) + 1, 2),0)
    print('Done\n\n')

    return Word_PMIVec



'''
Finding all the good comparisons for the target words
'''
def compare(params, attMap, CountDict):

    print('Calculating results:')

    #calc PMIVector for each word using counting
    PMIVectors=CalcWordVecPMI(CountDict)

    #declare Vars;
    tagIdx=params.tagIdx
    v2w = params.vector_to_word

    # each word has a counter with all the other words...(more explained in the compareVec function)
    count_features = {}

    '''
    this is a dictionary where for each word we have an entry ,
    and this entry will contain all values of the cosine of that word with all the other words.
    '''
    similarities_dict = {}

    print ('Comparing PMI vectors(please wait few minutes)\n')

    for word in tagIdx:
        similarities_dict[word], count_features[word] = compareVec(word, PMIVectors, attMap,v2w)
        print('Done')

    print('\n\n')
    print ('Results!:\n')
    for word in similarities_dict:
        k = 20
        sorted_attributes = sorted([attr for attr in similarities_dict[word] if count_features[word][attr] >3 ],
                                   key=lambda attr: similarities_dict[word][attr], reverse=True)
        sorted_pmi = sorted([attr for attr in PMIVectors[word]], key=lambda attr: PMIVectors[word][attr], reverse=True)
        print ("target word is: " + v2w[word])

        print ('First Order:')
        print (', '.join("%s" % (v2w[att[0]]) if type(att)==tuple else v2w[att] for att in sorted_pmi[:k]))

        print('Second Order: (most similar words) ')
        print (', '.join("%s" % (v2w[att[0]]) if type(att)==tuple else v2w[att] for att in sorted_attributes[:k]))
        print ('\n')



'''
Compare 2 PMIVectors using cosine and efficient multiply like we learned in lecture 6 
'''
def compareVec(currWord, PMIVectors, attMap,v2w):

    print('Checking similar words for: ' + v2w[currWord])

    # a dict for each attribute how meny times it occurs with currWord
    count_attributes = {}

    # a dict for each attribute of the cosine value with currWord
    word__cosine_val_dict = {}

    # going over all the attributes in PMIVector of a word
    for att in PMIVectors[currWord]:

        # we don't want compare to equal words...
        attributes=[att for att in attMap[att] if att !=currWord]

        # calc the cosine
        calcCosine(attributes,PMIVectors,currWord,att,word__cosine_val_dict,count_attributes)

    # adding the division of the vectors to cosine
    CosineHelp(PMIVectors,currWord,word__cosine_val_dict)

    return word__cosine_val_dict, count_attributes


'''
Calc the cosine without the divisor

'''
def calcCosine(attributes,PMIVectors,currWord,att,word__cosine_val_dict,count_features):

    # going over all the words that usually comes with the att
    for word in attributes:

        # same variable names like the lecture
        qi = PMIVectors[currWord][att]
        pi = PMIVectors[word][att]

        # if this word don't have a cosine value with currWord
        if word not in word__cosine_val_dict:
            word__cosine_val_dict[word] = 0

        # if this word don't have a counter with currWord
        if word not in count_features:
            count_features[word] = 0

        # adding to the cosine value and counter
        word__cosine_val_dict[word] += qi * pi
        count_features[word] += 1


'''
Updating cosine values by divding them by the length of the vectors(like in the formula)
'''
def CosineHelp(PMIVectors, currWord, word_CosineVal_dict):

    for word in word_CosineVal_dict:
        # calculating the length of each vector like in the formula
        sum1 = 0.0
        for u in PMIVectors[currWord]:
            sum1 += np.sqrt(PMIVectors[currWord][u] * PMIVectors[currWord][u])
        sum2 = 0.0
        for u in PMIVectors[word]:
            sum2 += np.sqrt(PMIVectors[word][u] * PMIVectors[word][u])

        #dividing by the length of the vectors like the formula
        word_CosineVal_dict[word] = word_CosineVal_dict[word] / (sum1 * sum2)



if __name__ == '__main__':
    main()