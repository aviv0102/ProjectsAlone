'''
Aviv shisman
Rom Sharon
'''


import numpy as np
import random
from sklearn.svm import SVR

def main():

    # creating model and training it
    np.random.seed(0)
    X,Y=generateData()
    SvmRegressor = SVR(gamma='scale', C=1.0, epsilon=0.2)
    SvmRegressor.fit(X, Y)

    # prediction and accuracy
    pred(SvmRegressor)

    return


'''
predict and get accuracy of model
'''
def pred(model):

    # vars and predict
    counter = 0
    size = 0
    test_x,tags=generateData()
    predictions = model.predict(test_x)

    # get accuracy
    for pred,tag in zip(predictions, tags):

        if (abs(pred-tag)<1):
            counter += 1
        size+=1

    print("Accuracy of a model: {}%".format(str(100.0 * counter / size)))


def generateData():
    np.random.seed(0)
    X=[]
    Y=[]
    for i in range (1,10000):
        # for input format of linear model
        y=[]
        x=[]

        # create data
        for j in range(0,10):
            x.append(random.randint(1,10))

        y.append(applyDataHypothesis(x))

        X.append(x)
        Y.append(y[0])
    return  np.array(X),np.array(Y)


def applyDataHypothesis(data):
    res=0
    for d in data:
        res+= d

    return res/len(data)


if __name__=='__main__':
    main()