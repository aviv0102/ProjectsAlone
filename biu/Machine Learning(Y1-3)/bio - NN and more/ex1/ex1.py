"""""
                    written by
name: Aviv Shisman              name: Itay Hassid 
id:   206558157                 id:   209127596
"""""

# imports:
import numpy as np
import random

# model params:
learningRate = 0.001
hidden_layer = 256
epoches = 60
input_layer = 3072
output_layer = 10

def activation_function(x):
    return np.divide(1, 1 + np.exp(-x))


"""""
A simple NN :)
"""""

def main():
    # loading data
    print('Loading data it might take a few moments...')
    trainSet = loadData("data/train.csv", "train", test=False)
    validSet = loadData("data/validate.csv", "validation", test=False)
    testSet = loadData("data/test.csv", "test", test=True)

    # creating the weights :
    w1 = np.random.uniform(-0.08, 0.08, [hidden_layer, input_layer])
    w2 = np.random.uniform(-0.08, 0.08, [output_layer, hidden_layer])
    b1 = np.random.uniform(-0.08, 0.08, [hidden_layer, 1])
    b2 = np.random.uniform(-0.08, 0.08, [output_layer, 1])
    weights = {'W1': w1, 'W2': w2, 'b1': b1, 'b2': b2}

    # train ...
    print('\nTrain!\n')
    weights = train(weights, trainSet, validSet)
    test(weights, testSet)

    return


'''
Training the model
'''


def train(weights, trainSet, validSet):
    global learningRate
    for i in range(epoches):
        print("epoch: ", i + 1)
        # shuffle each epoch?
        random.shuffle(trainSet)

        for ex in trainSet:
            sample = ex[0]
            tag = int(ex[1]) - 1

            # feedForward in the NN and calc loss
            params = feedForward(weights, sample, tag)

            # using back-prop to find gradients and improve weights using sgd
            gradients = back_propegation(weights, params)
            weights = update_weights(weights, gradients, learningRate)

        # validation:
        if i % 3 == 0:
            validation_loss, accurate = accuracy_on_validation(weights, validSet)
            print('epoch ' + str(i + 1) + ' results:\n')
            print("Accuracy of a model: {}%".format(str(100.0 * accurate)))
            print("loss: {}\n".format(str(100.0 * validation_loss)))

        # learningRate = learningRate * 0.99
        # print('learning rate', learningRate)

    return weights


'''
Test the model
'''

def test(weights, testSet):
    def softmaxTest(x):
        exps = np.exp(x - x.max())
        return exps / exps.sum()

    res = []
    b1 = weights['b1']
    b2 = weights['b2']
    W1 = weights['W1']
    W2 = weights['W2']

    for ex in testSet:
        # dropout
        prob = 0.5

        # doing feedForWard
        example = np.reshape(ex, (input_layer, 1))
        # layer 1
        z1 = np.dot(W1, example) + b1
        h1 = activation_function(z1)
        # h1 *= prob

        # layer 2
        z2 = np.dot(W2, h1) + b2
        h2 = softmaxTest(z2)
        # print(h2)
        y_hat = h2.argmax(axis=0)[0]
        res.append(str(y_hat + 1))
    with open('output.txt', 'w') as output:
        output.write('\n'.join(res))



"""""
Feedforward through the NN , applying activation function and softmax...
"""""
def feedForward(weights, example, y):
    # getting params
    b1 = weights['b1']
    b2 = weights['b2']
    W1 = weights['W1']
    W2 = weights['W2']

    # dropout
    prob = 0.8

    # doing feedForWard
    example = np.reshape(example, (input_layer, 1))
    # layer 1
    z1 = np.dot(W1, example) + b1
    h1 = activation_function(z1)
    # if training:
    do = np.random.binomial(1, prob, size=h1.shape) / prob
    # else:
    #     do = prob
    h1 *= do

    # layer 2
    z2 = np.dot(W2, h1) + b2
    ytag_y, softmax = softMax(z2, y)

    # saving Results:
    params = {'ytag_y': ytag_y, 'softmax': softmax, 'x': example, 'y': y, 'z1': z1, 'z2': z2, 'h1': h1, 'do': do}

    return params


"""""
softmax function
"""""

def softMax(x, y):
    exps = np.exp(x - x.max())
    exps = exps / exps.sum()

    ytag_y = exps[y][0]

    return (ytag_y, exps)


"""""
Back-prop, find the parameters...
"""""


def back_propegation(weights, params):
    # getting info
    w2 = weights['W2']
    h1 = params['h1']
    z1 = params['z1']
    example = params['x']
    classification = params['y']
    softmaxVec = params['softmax']
    do = params['do']

    # creating the one-dot vector of the right classification
    y = np.zeros((output_layer, 1))
    y[classification] = 1  # we decrease 1 to y because the vector is from 0 to 9 not 1 to 10

    # calculating the gradinets :
    dz2 = (softmaxVec - y)  # dL/dz2
    dW2 = np.dot(dz2, h1.T)  # dL/dz2 * dz2/dw2
    db2 = dz2  # dL/dz2 * dz2/db2
    dz1 = np.dot(w2.T, (softmaxVec - y)) * (1 - activation_function(z1)) * activation_function(
        z1) * do  # dL/dz2 * dz2/dh1 * dh1/dz1
    dW1 = np.dot(dz1, example.T)  # dL/dz2 * dz2/dh1 * dh1/dz1 * dz1/dw1
    db1 = dz1  # dL/dz2 * dz2/dh1 * dh1/dz1 * dz1/db1

    # return the gradients
    return {'dW1': dW1, 'dW2': dW2, 'db1': db1, 'db2': db2}

"""""
update the Weights using SGD method
"""""


def update_weights(weights, gradients, learningRate):
    W1 = weights['W1']
    W2 = weights['W2']
    b2 = weights['b2']
    b1 = weights['b1']

    dW1 = gradients['dW1']
    dW2 = gradients['dW2']
    db1 = gradients['db1']
    db2 = gradients['db2']

    W1 = W1 - learningRate * dW1
    W2 = W2 - learningRate * dW2
    b2 = b2 - learningRate * db2
    b1 = b1 - learningRate * db1

    weights = {'W1': W1, 'W2': W2, 'b1': b1, 'b2': b2}

    return weights

"""""
validation, check accuracy on validSet 
"""""


def accuracy_on_validation(weights, validSet):
    lossSum = 0
    successCounter = 0
    size = 0
    for ex in validSet:
        x = ex[0]
        y = int(ex[1]) - 1

        # Getting the NN prediction and calc loss:
        params = feedForward(weights, x, y)
        ytag_y = (params['ytag_y'])
        lossSum += calcLoss(ytag_y)

        # take highest probabilty
        y_hat = params['softmax'].argmax(axis=0)

        # check if correct
        if (y == y_hat[0]):  # we decrease 1 to y because the model learned to classify between 0 to 9
            successCounter += 1
        size += 1

    # sum up results:
    accuracy = successCounter / size * 1.0
    average_loss = lossSum / size * 1.0
    return average_loss, accuracy


'''
Load the different data files required for model
'''


def loadData(dataName, setName, test=False):
    split = lambda x: (x[1:], x[0])
    data = []
    dataFile = open(dataName, 'r')
    if test == False:
        for line in dataFile.readlines(): # [:10000]:
            train = np.fromstring(line, dtype=float, sep=',')
            data.append((train[1:], train[0]))
    else:
        for line in dataFile.readlines(): # [:100]:
            train = np.fromstring(line[2:], dtype=float, sep=',')
            data.append(train)

    print('done loading the ' + setName + ' set')
    return data


"""""
Loss, we already did sum.(ytag,y) -> so just apply -log
"""""


def calcLoss(ytag_y):
    return -np.log(ytag_y)


if __name__ == "__main__":
    main()
