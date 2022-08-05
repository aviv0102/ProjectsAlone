'''
       Aviv Shisman 206558157  Itay Hassid 209127596

       for more details read WriteUp file!
'''

from sklearn.datasets import fetch_mldata
from sklearn.utils import shuffle
import numpy as np
import math
import random


'''
Reading the Train x,y
'''
mnist = fetch_mldata("MNIST original", data_home="./data")
X, Y = mnist.data[:60000] / 225., mnist.target[:60000]
x = [ex for ex, ey in zip(X, Y) if ey in [0, 1, 2, 3]]
y = [ey for ey in Y if ey in [0, 1, 2, 3]]

x, y = shuffle(x, y, random_state=1)


'''
Getting Test x,y for acc measurement
'''
test_y = np.loadtxt('y_test.txt')
test_x = np.loadtxt('x_test.txt')
pred_x = np.loadtxt('x4pred.txt')
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
transform the labels of TagSet to correspond to the method (oneVsAll or AllPairs)
'''
def changeLabels(tags, selectedLabel,secondLabel,mode):
    newTags = list(tags)
    for i, t in enumerate(newTags):
        #oneVsAll
        if mode==0:
            newTags[i] = 1 if (t == float(selectedLabel)) else -1
        #allPairs
        if mode==1:
            if t==float(selectedLabel):
                newTags[i]=1
            elif t==float(secondLabel):
                newTags[i]=-1
            else:
                newTags[i]=0

    return newTags

'''
SVM trainer, to train multiple svm's
'''
class Trainer:
    def __init__(self):
        self.w = np.zeros((1, 784))
        # self.tags = tags

    def train(self, tags):
        w = self.w
        for i in range(1, epochs):
            currLr = lr/math.sqrt(i)
            for example,tag in zip(x, tags):
                score = 1-tag*np.dot(w, example)
                if score > 0:
                    w = (1 - currLr*lamda)*w + example * currLr * tag
                else:
                    w = (1 - currLr*lamda)*w
        self.w = w

    ''' 
    get prediction to measure acc%
    '''
    def pred(self, tags):
        counter = 0
        size=0
        #testing
        for i, ex in enumerate(test_x):
            pred=sign(np.dot(self.w, ex))
            if tags[i] == 0 :
                continue
            elif (pred == tags[i]): #test_y[i]):
                counter += 1
                size+=1
            elif pred==-1 or pred==0:
                size+=1


        print("Accuracy of a single SVM: {}%".format(str(100.0*counter/size)))

    def getW(self):
        return self.w

def main():
    OneVsAll()
    allPairs()
    randomMatrix()
    return

'''
Train OneVsAll classifiers and sending them to hamming and loss decoding for prediction (read more in WriteUp file)
'''
def OneVsAll():
    matrix = np.matrix([[1, -1, -1, -1], [-1, 1, -1, - 1], [-1, -1, 1, -1], [-1, -1, -1, 1]])
    trainers=[]

    # train models and create them
    print('oneVsAll train:\n\n')
    for j in range(4):
        new_y = changeLabels(y, j,0,0)
        new_test_y = changeLabels(test_y, j,0,0)
        svm = Trainer()
        svm.train(new_y)
        svm.pred(new_test_y)
        trainers.append(svm)
    hamming(trainers,test_x,test_y,matrix,'',0)
    lossDecoding(trainers,test_x,test_y,matrix,'',0)

    hamming(trainers, pred_x, None, matrix, 'test.onevall.ham.pred',1)
    lossDecoding(trainers, pred_x,None, matrix, 'test.onevall.loss.pred',1)

'''
Train AllPairs classifiers and sending them to hamming and loss decoding for prediction (read more in WriteUp file)

'''
def allPairs():
    #all pairs:             1Vs2             1Vs3             1Vs4         2Vs3        2Vs4            3Vs4
    matrix = np.matrix([[1,1 ,1,0,0,0], [-1, 0, 0, 1, 1, 0], [0, -1, 0, -1, 0, 1], [0, 0, -1, 0, -1, -1]])
    trainers=[]

    # train models and create them
    visited=[]
    print ("AllPairs Train:\n\n")
    for i in range(4):
        for j in range(4):
            if (i,j) in visited or i==j:
                continue
            else:
                visited.append((i,j))
                visited.append((j,i))
                new_y = changeLabels(y, i,j,1)
                new_test_y = changeLabels(test_y, i,j,1)
                svm = Trainer()
                svm.train(new_y)
                svm.pred(new_test_y)
                trainers.append(svm)


    hamming(trainers,test_x,test_y,matrix,'',0)
    lossDecoding(trainers,test_x,test_y,matrix,'',0)

    hamming(trainers,pred_x,None,matrix,'test.allpairs.ham.pred',1)
    lossDecoding(trainers,pred_x,None,matrix,'test.allpairs.loss.pred',1)


'''
Hamming Decoding simple implementation like in class
'''
def hamming(trainers,examples, tags, matrix,ModelName,TestFlag):
    count = 0
    if TestFlag==1:
        modelout=open(ModelName,'w')
    for i, x_sample in enumerate(examples):
        binaryVec = []
        for trainer in trainers:
            binaryVec.append(np.dot(trainer.getW(), x_sample))

        minVal = np.inf
        minArg = 0
        for j, line in enumerate(matrix):   #for each row/class
            sum = 0
            line=np.ravel(line)
            for k, bit in enumerate(line):  #moving each col?(get each classifier output and calc hamming)
               sum += (1 - sign(bit*binaryVec[k]))/2
            if sum<minVal:
                minVal=sum
                minArg=j
        if TestFlag==0:
            if minArg==tags[i]:
                count+=1
        if TestFlag==1:
            modelout.write(str(minArg)+'\n')


    if TestFlag==0:
        size=len(tags)
        print("Hamming Accuracy: {}%".format(str(100.0 * count / size)))
    else:
        modelout.close()


    return

'''
Loss Decoding simple implementation like in class(replace one line actually for Svm loss instead of hamming...)
'''
def lossDecoding(trainers,examples, tags, matrix,ModelName,TestFlag):
    count = 0
    if TestFlag==1:
        modelout = open(ModelName, 'w')
    for i, x_sample in enumerate(examples):
        binaryVec = []
        for trainer in trainers:
            binaryVec.append(np.dot(trainer.getW(), x_sample))

        minVal = np.inf
        minArg = 0
        for j, line in enumerate(matrix):   #for each row/class
            sum = 0
            line=np.ravel(line)
            for k, bit in enumerate(line):  #moving each col?(get each classifier output and calc hamming)
               sum +=  max(1-(bit*binaryVec[k]),0)
            if sum<minVal:
                minVal=sum
                minArg=j
        if TestFlag==0:
            if minArg == tags[i]:
                count += 1
        if TestFlag==1:
            modelout.write(str(minArg) + '\n')


    if TestFlag==0:
        size = len(tags)
        print("Loss Accuracy: {}%".format(str(100.0 * count / size)))
    else:
        modelout.close()
    return

'''
Random Matrix, generate the random matrix with random values of 1,0,-1 and random number of classifiers(cols)
'''
def randomMatrix():

    numberOfModels=random.randint(2,6)
    matrix = np.zeros(shape=(4, numberOfModels))
    for i, line in enumerate(matrix):  # for each row/class
        for j, bit in enumerate(line):
            matrix[i][j]=random.randint(-1,1)

    # train models and create them
    print('Train Random Matrix Trainers:\n\n')
    trainers = []
    for col in range(np.size(matrix,1)):
        dict={}
        j=0
        for cell in matrix[:, col]:
            dict[j]=int(cell)
            j+=1
        newY=randomMatrixLabelChange(y,dict)
        new_test_y = randomMatrixLabelChange(test_y,dict)
        svm = Trainer()
        svm.train(newY)
        svm.pred(new_test_y)
        trainers.append(svm)

    print('Random Matrix predictions:\n')
    hamming(trainers, test_x,test_y, matrix,'',0)
    lossDecoding(trainers,test_x, test_y, matrix,'',0)

    hamming(trainers,pred_x, None, matrix,'test.randm.ham.pred',1)
    lossDecoding(trainers,pred_x, None, matrix,'test.randm.loss.pred',1)

    return


'''
help function
'''
def randomMatrixLabelChange(tags,dict):
    newTags = list(tags)
    for i, t in enumerate(newTags):
        newTags[i] = dict[int(t)]

    return newTags



if __name__=='__main__':
    main()