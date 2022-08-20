'''
       Aviv Shisman 206558157  Itay Hassid 209127596

       for more details read WriteUp file!
'''

import numpy as np
import random
import sys

### set hyper-parameters
epochs = 13

def main():

    if len(sys.argv)!=3:
        print('error, not in format')
        print('Enter 2 arguments: TrainFile TestFile')
        return

    print('LoadInfo...')
    train,test=loadInfo(sys.argv[1],sys.argv[2])
    # MCPerceptron(train,test)
    MCStructuredPerceptron(train, test)

    return
'''
Load the inputs
'''
def loadInfo(trainName,testName):

    train=open(trainName,'r')
    trainInput=[]
    for line in train.readlines():
        row=line.split()
        current=[]
        current.append(row[0])  #character id
        current.append(row[1])  # character (Yi)
        current.append(row[2])  # next character id
        current.append(row[3])  # word id
        current.append(row[4])  # position of letter
        current.append(row[5])  # cross validation fold
        current.append([int(i) for i in row[6:]])  # vector
        trainInput.append(current)

    testInput=[]
    test=open(testName,'r')
    for line in test.readlines():
        row = line.split()
        current = []
        current.append(row[0])  # character id
        current.append(row[1])  # character (Yi)
        current.append(row[2])  # next character id
        current.append(row[3])  # word id
        current.append(row[4])  # position of letter
        current.append(row[5])  # cross validation fold
        current.append([int(i) for i in row[6:]])  # vector
        testInput.append(current)

    return trainInput,testInput

'''
model 1, regular multiclass perceptron
'''
def MCPerceptron(train,test):

    print('Model 1 Training...')
    ws = np.zeros((26, 128))
    sumWS = np.zeros((26, 128))
    for i in range(epochs):
        random.shuffle(train)
        for currExample in train:

            x = currExample[6]
            y = ord(currExample[1]) - 97    # tag
            max = -np.inf
            maxidx = 0
            for i, w in enumerate(ws):
                res = np.dot(w, x)
                if res > max:
                    max = res
                    maxidx = i
            y_tag = maxidx

            if y != y_tag:
                ws[y] += x
                ws[y_tag] -= x
        sumWS += ws
        ws = np.zeros((26, 128))

    sumWS /= (epochs * len(train))
    predModel1(sumWS, test)

    return

''' 
get prediction to measure acc%
'''
def predModel1(ws, test):

    print('prediction...')
    counter = 0
    size = 0
    for currExample in test:
        # x = [int(i) for i in currExample[6]]  # the binary pixel representation
        x = currExample[6]
        y = ord(currExample[1]) - 97          # tag
        max = -np.inf
        maxidx = -1
        for i, w in enumerate(ws):
            res = np.dot(w, x)
            if res > max:
                max = res
                maxidx = i
        y_tag = maxidx
        if y == y_tag:
            counter += 1
        size += 1

    print("Accuracy: {}%".format(str(100.0*counter/size)))

'''
model 2, Structured Perceptron
'''
def MCStructuredPerceptron(train,test):
    print('Model 2 Training...')
    w = np.zeros((1, 26 * 128))
    sumW = np.zeros((1, 26 * 128))
    for i in range(1, epochs):
        random.shuffle(train)
        for currExample in train:

            y = ord(currExample[1]) - 97  # tag
            # max arg
            maxval = -np.inf
            maxidx = 0
            for i in range(26):
                x = features(currExample, i)  # the binary pixel representation
                res = np.dot(w, x)
                if res > maxval:
                    maxval = res
                    maxidx = i
            y_tag = maxidx

            if y != y_tag:
                w = w + features(currExample, y) - \
                    features(currExample, y_tag)
        sumW += w
        w = np.zeros((1, 26 * 128))
    sumW /= (epochs * len(train))
    predModel2(sumW, test)
    return

'''
features function
'''
def features(currExample, yi):
    x = currExample[6]
    vec = np.zeros((26 * 128,))
    vec[yi*128: yi*128 + 128] = x
    return vec

'''
getting model2 accuracy %
'''
def predModel2(w, test):

    print('prediction...')
    f = open('multiclass.pred', 'w')
    counter = 0
    size = 0

    for currExample in test:

        y = ord(currExample[1]) - 97  # tag
        maxval = -np.inf
        maxidx = 0
        for i in range(26):
            x = features(currExample, i)  # the binary pixel representation
            res = np.dot(w, x)
            if res > maxval:
                maxval = res
                maxidx = i
        y_tag = maxidx
        f.write('{}\n'.format(chr(y_tag+97)))
        if y == y_tag:
            counter += 1
        size += 1
    f.close()

    print("Accuracy: {}%".format(str(100.0*counter/size)))

if __name__ == '__main__':
    main()
