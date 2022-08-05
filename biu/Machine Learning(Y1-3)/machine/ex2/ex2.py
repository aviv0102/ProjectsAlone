# aviv shisman 206558157
import numpy as np
import random
import matplotlib.pyplot as plot
from matplotlib.legend_handler import HandlerLine2D
import math

def main():
    """""
    i used the pseudo code from the piazza combined with the theortical part formula to write the training.
    the code is divided to different section of the algorithem + functions for implementing the training.
    """""
    # generate X:
    a =np.random.normal(2,1,100);
    b =np.random.normal(4,1,100);
    c =np.random.normal(6, 1, 100);
    X=list();
    #adding all to X
    X.extend(a);
    X.extend(b);
    X.extend(c);

    # generate Y(the classifications) ,W&b(for the SGD algorithem)
    Y =[i/100 +1 for i in range(300)];
    W =[0,0,0];
    b =[0,0,0];
    learningRare=0.1;
    updateW=0;
    updateB=0;

    #training start, number of epochs can be changed
    epoch=20;
    for i in range (epoch):
        #shuffle
        Shuff=list(zip(X,Y));
        random.shuffle(Shuff);
        X,Y=zip(*Shuff);

        # applying the SGD
        for x,y in zip(X,Y):
            # calculating the update by the formula from the theory part
            for i in range(0, 3):
                if i+1 == y:
                    updateW = -x + softMax(i, W, x, b) * x;
                    updateB= -1 + softMax(i, W, x, b);
                else:
                    updateW = softMax(i, W, x, b) * x;
                    updateB = softMax(i, W, x, b);

                # update Results
                b[i] = b[i] - learningRare *updateB;
                W[i] = W[i] - learningRare *updateW;

    printGraph(W,b);

    return 0;

#the softMax, used to calculate w&b and predict
def softMax(i,w,x,b):

    first=np.exp(w[i]*x+b[i]);
    second=np.exp(w[0]*x+b[0])+np.exp(w[1]*x+b[1])+np.exp(w[2]*x+b[2]);
    if(second ==0):
        return 0;

    result=first/second;

    return result;
#density
def density(m, x):
    return ( np.exp((-(x-m)**2)/2)*(1/math.sqrt(2*math.pi)) );

#printing the graph
def printGraph(w,b):
    # creating dictionaries for each function
    PredDict ={}
    RightDict = {}
    for x in range(0,11):
        #predict
        PredDict[x] = softMax(0,w,x,b)
        #real values
        RightDict[x] = (density(2, x)) / (density(2, x) + density(4, x) + density(6, x))

    #drawing the graph
    label1, =plot.plot(PredDict.keys(), PredDict.values(), "g-", label='Softmax Distribution')
    label2, =plot.plot(RightDict.keys(), RightDict.values(), "b-", label='Real normal Distribution')
    plot.legend(handler_map = {label1:HandlerLine2D(numpoints=6)});
    plot.show();




if __name__ == "__main__":
    main()