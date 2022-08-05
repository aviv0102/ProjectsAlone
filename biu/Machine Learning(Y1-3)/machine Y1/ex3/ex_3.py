"""""
name: Aviv Shisman
id:   206558157
"""""


#imports:
import numpy as np


"""""
Main
"""""
def main():

    """""
    Getting the info and creating the Parameters.
    """""
    print "Read Info: ..."
    classifications = np.loadtxt("train_y")
    examples = np.loadtxt("train_x")
    test = np.loadtxt("test_x")

    #hyper parameters:
    learningRate=0.01
    hiddenLayerSize=50
    epochesNumber=22
    activation_function = lambda x: np.divide(1,1+np.exp(-x))

    #spliting to %80-%20: (example & classifications take 80%, validation_x and y takes 20)
    validationSize=int(len(examples)*0.2)
    validation_x = examples[-validationSize:, :]
    validation_y=classifications[-validationSize:]
    examples = examples[:-validationSize, :]
    classifications=classifications[:-validationSize]

    # shuffle:
    examples,classifications=shuffle(examples,classifications)
    validation_x,validation_y=shuffle(validation_x,validation_y)

    #normalization
    examples=examples/255
    validation_x = validation_x/255
    test=test/255

    #creating W1,W2,b1,b2:
    numberOfPixels=784;
    w1 = np.random.uniform(-0.08,0.08,[hiddenLayerSize, numberOfPixels])
    w2 = np.random.uniform(-0.08,0.08,[10, hiddenLayerSize])
    b1 = np.random.uniform(-0.08,0.08,[hiddenLayerSize,1])
    b2 = np.random.uniform(-0.08,0.08,[10,1])
    ourParameters = {'W1': w1, 'W2': w2, 'b1': b1, 'b2': b2}

    print "Training begun: ...\n\n"
    """""
    Training the Model:
    """""
    for i in range(epochesNumber):
        lossSum=0.0;
        examples,classifications=shuffle(examples,classifications)
        for example,classification in zip(examples,classifications):
            #feedForward in the NN and calc loss
            feedParams=feedForward(ourParameters,activation_function,example,classification,numberOfPixels)
            ytag_y = (feedParams['ytag_y'])
            lossSum+=calcLoss(ytag_y)

            #using back-prop to find gradients and improve parametes using sgd
            gradients=back_propegation(feedParams)
            ourParameters=updateParamsSGD(ourParameters,gradients,learningRate)



        # validation time:
        validation_loss, accurate = validation(ourParameters,activation_function,
                                               validation_x,validation_y,numberOfPixels)
        print accurate*100



    print "Test\n\n"
    """""
    Test Time :)
    Doing the prediction with 0 as classfication(it doesn't matter because we don't calc loss)
    """""
    pred_file = open("test.pred", 'w')
    for x in test:
        feedParams = feedForward(ourParameters, activation_function, x, 0, numberOfPixels)
        y_hat = feedParams['softmax'].argmax(axis=0)
        pred_file.write(str(y_hat[0]) + "\n")
    pred_file.close()
    return 0;




"""""
softmax function
"""""
def softMax(w,x,b,y):

    # calculate the sum
    softmax = np.zeros((10, 1))
    vec = [np.exp(np.dot(wi, x) + bi) for wi, bi in zip(w, b)]
    sum=np.sum(vec);

    #calc softMax
    for i in range(10):
        softmax[i] = np.exp(np.dot(w[i], x) + b[i]) / sum

    #getting the probabilty for the loss later
    #because y is all zeros except 1, i will use only the 1 spot and take it out of the vector
    ytag_y=softmax[y][0]

    return (ytag_y,softmax)


"""""
feedForward, calculate the probality using softmax
"""""
def feedForward(params,function,example,y,numOFpix):
    # doing feedForWard
    example = np.reshape(example, (1,numOFpix))
    x = np.transpose(example)

    b1=params['b1']
    b2=params['b2']
    W1=params['W1']
    W2=params['W2']


    z1 = np.dot(W1, x) + b1
    h1 =function(z1)
    z2 = np.dot(W2, h1) + b2

    #saving Results and calculating softmax:
    ytag_y,softmax=softMax(W2,h1,b2,y);
    params['ytag_y']=ytag_y;
    params['softmax']=softmax;
    params['x']=x;
    params['y']=y;
    params['z1']=z1;
    params['z2']=z2;
    params['h1']=h1;


    return params


"""""
Back-prop, find the parameters...
"""""
def back_propegation(feedParams):
    # getting params
    h1=feedParams['h1']
    example=feedParams['x']
    w2=feedParams['W2']
    classification=feedParams['y']
    softmaxVec=feedParams['softmax']


    #creating the one-dot vector of the right classification
    y = np.zeros((10, 1))
    y[classification] = 1

    #calculating the gradinets:
    dz2 = (softmaxVec - y)                               # dL/dz2
    dW2 = np.dot(dz2, h1.T)                              # dL/dz2 * dz2/dw2
    db2 = dz2                                            # dL/dz2 * dz2/db2
    dz1 = np.dot(w2.T,(softmaxVec - y)) *(1 - h1)* h1    # dL/dz2 * dz2/dh1 * dh1/dz1
    dW1 = np.dot(dz1, example.T)                         # dL/dz2 * dz2/dh1 * dh1/dz1 * dz1/dw1
    db1 = dz1                                            # dL/dz2 * dz2/dh1 * dh1/dz1 * dz1/db1


    #return the gradients
    return { 'dW1': dW1,'dW2': dW2, 'db1': db1,'db2': db2 }


"""""
Loss, we already did sum.(ytag,y) -> so just apply -log
"""""
def calcLoss(ytag_y):
    return -np.log(ytag_y)



"""""
shuffle
"""""
def shuffle(x,y):
    shape = np.arange(x.shape[0])
    np.random.shuffle(shape)
    x ,y= x[shape],y[shape]

    return (x,y);



"""""
update the params using SGD
"""""
def updateParamsSGD(params,gradients,learningRate):

    W1=params['W1']
    W2=params['W2']
    b2=params['b2']
    b1=params['b1']

    dW1=gradients['dW1']
    dW2=gradients['dW2']
    db1=gradients['db1']
    db2=gradients['db2']
    W1 = W1 - learningRate * dW1
    W2 = W2 - learningRate * dW2
    b2 = b2 - learningRate * db2
    b1 = b1 - learningRate * db1

    return {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}



"""""
validation stage:
1.doing feedForward and calculating loss
2.getting ytag from softmax and find if y!=ytag
3.sum results -> get acc of model
"""""
def validation(params, activation_function, validation_x, validation_y,numofPix):
    lossSum = 0
    successCounter = 0
    for x, y in zip(validation_x,validation_y):
        # Getting the NN prediction and calc loss:
        feedParams = feedForward(params, activation_function, x, y,numofPix)
        ytag_y = (feedParams['ytag_y'])
        lossSum += calcLoss(ytag_y)

        #take highest probabilty
        y_hat = feedParams['softmax'].argmax(axis=0)

        #check if correct
        if (y == y_hat[0]):
            successCounter += 1

    # sum up results:
    accuracy = successCounter / float(np.shape(validation_x)[0])
    average_loss = lossSum / np.shape(validation_x)[0]
    return average_loss, accuracy



if __name__ == "__main__":
    main()