'''
       Aviv Shisman 206558157  Itay Hassid 209127596

       for more details read WriteUp file!
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import sys

### set hyper-parameters
epochs = 8

def main():

    if len(sys.argv) != 3:
        print('error, not in format')
        print('Enter 2 arguments: TrainFile TestFile')
        return

    print('LoadInfo...')
    train,test=loadInfo(sys.argv[1],sys.argv[2])

    model3(train,test)

    return

'''
Load the inputs
'''
def loadInfo(trainName,testName):

    train = open(trainName,'r')
    trainInput = []
    for line in train.readlines():
        row = line.split()
        current = []
        current.append(row[0])  #character id
        current.append(row[1])  # character (Yi)
        current.append(row[2])  # next character id
        current.append(row[3])  # word id
        current.append(row[4])  # position of letter
        current.append(row[5])  # cross validation fold
        current.append([int(i) for i in row[6:]])  # vector
        trainInput.append(current)

    testInput = []
    test = open(testName,'r')
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

    return trainInput, testInput

'''
model 3
'''
def model3(train, test):
    print('Model 3 Training...\n')
    w = np.zeros(26 * 128 + 27 * 27)
    sumW = np.zeros(26 * 128 + 27 * 27)
    words = load_words(train)

    for i in range(epochs):
        random.shuffle(words)
        for j, example in enumerate(words):
            if j % 100 == 0:
                print(str((1-j/len(words))*100)+'% left to finish epoch')

            word = example[0]
            y = example[1]
            y_hat = viterbi(word, w)
            tags=[]
            for i in range(len(y_hat)):
                tags.append(chr(y_hat[i]+97))
            w = w + build_phi(word, y) - build_phi(word, tags)
        sumW += w
        w = np.zeros(26 * 128 + 27 * 27)
    sumW /= (epochs * len(train))
    predModel3(sumW, test)
    plot_heatmap(sumW[26*128:])


def viterbi(word, w):

    # return y_hat
    num_of_eng_char = 26
    label_size = len(word)
    d_s = np.zeros((label_size, num_of_eng_char))
    d_pi = np.zeros((label_size, num_of_eng_char))

    # Initialize
    prev_char = chr2idx('$')
    for i in range(num_of_eng_char):
        curr_char = i   # chr2idx(chr(97 + i))
        phi = features3(word[0][6], curr_char, prev_char)
        s = np.dot(w, phi)
        d_s[0][i] = s
        d_pi[0][i] = 0

    # Recursion
    for i in range(1, label_size):
        for j in range(num_of_eng_char):
            curr_char = j   # chr2idx(chr(97 + j))
            d_best = -float("inf")
            i_best = -1
            for ytag in range(num_of_eng_char):
                phi = features3(word[i][6], curr_char, ytag)
                res = np.dot(w, phi) + d_s[i-1][ytag]
                if res > d_best:
                    d_best = res
                    i_best = ytag
            d_s[i][j] = d_best
            d_pi[i][j] = i_best
    # backtrack
    y_hat = np.zeros((label_size,)).astype(int)
    d_best = -float("inf")
    for i in range(num_of_eng_char):
        if d_best < d_s[label_size - 1][i]:
            y_hat[label_size - 1] = i
            d_best = d_s[label_size - 1][i]

    for i in range(label_size - 2, -1, -1):
        y_hat[i] = d_pi[i + 1][y_hat[i + 1]]
    return y_hat

def chr2idx(x):
    if str.isalpha(x):
        return ord(x) - 97
    return 26

'''
x: letter
y: tag
prevY: previous tag
'''
def features3(x, y, prevY):
    vec = np.zeros((26 * 128 + 27 * 27,))
    vec[y * 128 : y * 128 + 128] = x
    vec[26 * 128 + 27 * prevY + y] = 1
    return vec

def build_phi(word, y):
    prev_char = chr2idx('$')
    w = np.zeros((26 * 128 + 27 * 27,))
    for i, letter in enumerate(word):
        # w += features3(letter[6], chr2idx(y[i]), prev_char)
        yi = chr2idx(y[i])
        w[yi*128 : yi*128 + 128] += letter[6]
        w[128*26 + 27 * prev_char + yi] += 1
        prev_char = chr2idx(y[i])

    return w

def predModel3(w, test):

    print('prediction...')
    f = open('structured.pred', 'w')
    counter = 0
    size = 0

    #testing
    word = []
    y = []
    for example in test:
        word.append(example)
        y.append(example[1])
        if example[2] != '-1':
            continue
        y_hat = viterbi(word, w)

        tags = []
        for i in range(len(y_hat)):
            tags.append(chr(y_hat[i] + 97))
        for real_tag, pred_tag in zip(y, tags):
            f.write('{}\n'.format(pred_tag))
            if real_tag == pred_tag:
                counter += 1
            size += 1
        word = []
        y = []
    f.close()

    print("Accuracy: {}%".format(str(100.0*counter/size)))

def load_words(train):
    words = []
    word = []
    y = []
    for j, example in enumerate(train):
        word.append(example)
        y.append(example[1])
        if example[2] == '-1':
            words.append((word, y))
            word = []
            y = []
    return words

def plot_heatmap(feature_array):
    matrix = np.reshape(feature_array, (27, 27))
    matrix = matrix[:-1, :-1]
    x = [chr(i + 97) for i in range(26)]
    y = [chr(i + 97) for i in range(26)]

    fig, ax = plt.subplots()
    im = ax.imshow(matrix, cmap='Greys')
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x)))
    ax.set_yticks(np.arange(len(y)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x)
    ax.set_yticklabels(y)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), ha="right", rotation_mode="anchor")

    ax.set_title('Characters transition Parameters')
    fig.tight_layout()
    plt.show()


if __name__=='__main__':
    main()
