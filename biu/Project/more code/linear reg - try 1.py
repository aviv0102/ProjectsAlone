# imports
import numpy as np
from sklearn.linear_model import LinearRegression
import random

def main():

    # generate data and creating the model
    X,Y = generateData()
    regression_model = LinearRegression()

    # training
    regression_model.fit(X, Y)

    # Predict
    y_predicted = regression_model.predict(X)

    errorBound=0.001
    correct=0
    size=0
    for ytag,yi in zip( y_predicted,Y):
        if abs(ytag-yi)<errorBound:
            correct+=1
        size+=1

    print("Accuracy {}%".format(str(100.0 * correct / size)))



def generateData():
    np.random.seed(0)
    X=[]
    Y=[]
    what_we_had=[]
    for i in range (1,10000):
        # for input format of linear model
        if i==1:
            mid=random.randint(1,100)
        else:
            mid= getMid(Y)
        x=[]
        y=[]
        x.append(mid)
        y.append((2*mid+5))
        X.append(x)
        Y.append(y)

    return  np.array(X),np.array(Y)

def getMid(data):
    s=0
    t=0
    for d in data:
        s+=d[0]
        t+=1
    res = s/t
    return res

if __name__=='__main__':
    main()