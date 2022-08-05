
import numpy as np
import math
import random



### set hyper-parameters
lr = 0.001
epochs = 50
lamda = 0.1


'''
Sign func...
'''
def sign(val):
    if val > 0:
        return 1
    if val == 0:
        return 0
    return -1




'''
SVM trainer, to train multiple svm's
'''
class Trainer:
    def __init__(self):
        self.w = np.zeros((1, 10))
        # self.tags = tags

    def train(self):
        w = self.w
        x,tags=generateData()
        for i in range(1, epochs):
            currLr = lr/math.sqrt(i)
            for example,tag in zip(x, tags):
                score = 1-tag*np.dot(w, example)
                if abs(score-tag)>1:
                    w = (1 - currLr*lamda)*w +  currLr * (score-tag)
                else:
                    w = (1 - currLr*lamda)*w
        self.w = w

    ''' 
    get prediction to measure acc%
    '''
    def pred(self):
        counter = 0
        size=0
        #testing
        test_x,tags=generateData()
        for example, tag in zip(test_x, tags):
            pred=np.dot(self.w, example)
            if (abs(pred-tag)<1): #test_y[i]):
                counter += 1
            size+=1



        print("Accuracy of a single SVM: {}%".format(str(100.0*counter/size)))

    def getW(self):
        return self.w

def main():
    trainer=Trainer()
    trainer.train()
    trainer.pred()

    return

def generateData():
    np.random.seed(0)
    X=[]
    Y=[]
    for i in range (1,1000):
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

    return res


if __name__=='__main__':
    main()