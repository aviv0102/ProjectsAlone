'''
Itay Hassid 209127596  Aviv Shisman 206558157
'''

import librosa
import os
import numpy as np
from scipy import stats



def main():

    # intro
    print('Hello, this is Speech recognition - ex2\n')
    print('Please make sure you have:       ')
    print('1. train_data directory that contains the 25 examples organized in to 5 directories')
    print('2. test_files directory that contains the 250 examples you want the prediction for\n')
    print('*in case a problem occurs check our drive in details file\n')
    print('Thank you :)\n\n')


    # loading data
    print( 'Loading Data and extracting features...\n')
    train = load_data("train_data",0)
    test = load_data("test_files",1)

    # accuracy comment this before submit
    #print('accuracy... need to comment next 2 lines before submit')
    #tagged = load_data("testTagged",0)
    #getAccuracy(train,tagged)

    # prediction
    pred(train,test)
    print('done')

'''
loading the audio files from a directory and extracting mfcc features
'''
def load_data(libName,flag):


    # all the available dirs of audio files
    dirs = ["one", "two", "three", "four", "five"]
    data = []

    # in case we are in test_files and there is one big dir with all files
    if flag == 1:
        dirs=[""]
        path = libName + "/"

    for name in dirs:


        # get all audio files in each dir
        if name!="":
            path = libName + "/" + name + "/"


        files = [file for file in os.listdir(path) if os.path.isfile(path+"/"+file)]
        for f in files:
            src = "%s%s" % (path, f)
            if not src.endswith('wav'):
                continue
            if flag == 1:
                name = f    # we would like to write the file name in output.txt later in case of test_files

            # for each audio file we extract the mfcc object (transforming from time domain to freq)
            y, sr = librosa.load(src, sr=None)
            y = y/np.linalg.norm(y)

            mfcc = librosa.feature.mfcc(y=y, sr=sr)
            # mfcc = mfcc/np.linalg.norm(mfcc)
            mfcc = stats.zscore(mfcc)

            # normalizing for better results and adding the feature matrix(mfcc object) to data
            data.append((mfcc, name))


    return data

'''
get accuracy with tagged test_files for each method
'''
def getAccuracy(train,tagged):

    correct = size = 0

    for testEx in tagged:
        min_dis = np.inf
        min_arg = None
        for example in train:
            dist = DTW(example[0], testEx[0])
            if dist < min_dis:
                min_dis = dist
                min_arg = example[1]
        if min_arg==testEx[1]:
            correct+=1
        size+=1
    print("Accuracy of a DTW: {}%".format(str(100.0 * correct / size)))

    correct = size = 0

    for testEx in tagged:
        min_dis = np.inf
        min_arg = None
        for example in train:
            dist = euc_dis(example[0], testEx[0])
            if dist < min_dis:
                min_dis = dist
                min_arg = example[1]
        if min_arg == testEx[1]:
            correct += 1
        size += 1
    print("Accuracy of a Euc: {}%\n".format(str(100.0 * correct / size)))

    return


'''
method 1 - compare the 2 feature matrix with euclidian distance
'''
def euc_dis(mat1, mat2):
    sigma = 0
    for i in range(mat1.shape[1]):
        sigma += distance(mat1[:, i], mat2[:, i])
    sigma = 1.0 * sigma / mat1.shape[1]
    return sigma

'''
euclidian distance
'''
def distance(arr1, arr2):
    return np.linalg.norm(arr1 - arr2)

'''
method 2 -dynamic time warping algorithem - > align each feature matrix to the other so that we can compare them
'''
def DTW(mat1, mat2):
    table = np.ones((mat1.shape[1] + 1, mat2.shape[1] + 1))
    table[:, :] = np.inf
    table[0, 0] = distance(mat1[:,0], mat2[:,0])

    for i in range(1, mat1.shape[1] + 1):
        for j in range(1, mat2.shape[1] + 1):
            cost = distance(mat1[:,i - 1], mat2[:, j - 1])
            table[i, j] = cost + min(table[i - 1, j],
                                     table[i, j - 1],
                                     table[i - 1, j -1])
    return table[-1, -1]

'''
prediction for test_files files
'''
def pred(train,test):
    print('Writing prediction please wait few moments...\n')
    output = open('output.txt', 'w')

    # getting prediction for each test file
    for testEx in test:
        min_dis = np.inf
        min_arg = None

        st = testEx[1] + ' - '

        # prediction using euc_dis
        for example in train:
            dist = euc_dis(example[0], testEx[0])
            if dist < min_dis:
                min_dis = dist
                min_arg = example[1]
        st += min_arg + ' - '
        min_dis = np.inf

        # prediction using DTW
        for example in train:
            dist = DTW(example[0], testEx[0])
            if dist < min_dis:
                min_dis = dist
                min_arg = example[1]
        st += min_arg
        st+='\n'

        # writing results...
        output.write(st)


    output.close()


if __name__=="__main__":
    main()


