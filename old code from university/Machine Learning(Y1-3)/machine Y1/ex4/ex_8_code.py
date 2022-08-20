'''
name: Aviv shisman
id:   206558157
'''

#imports:
import torch
from torchvision import datasets, transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.sampler import SubsetRandomSampler
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D



'''
First model, multiclasses classifier(log softmax at the end)
Regular NN with 2 hidden layers using relu as
activation function 
'''
class A(nn.Module):

    def __init__(self,image_size,FL,SL):
        super(A, self).__init__()
        self.image_size = image_size
        self.fc0 = nn.Linear(image_size, FL)
        self.fc1 = nn.Linear(FL, SL)
        self.fc2 = nn.Linear(SL, 10)

    def forward(self, x):
        x = x.view(-1, self.image_size)
        x = F.relu(self.fc0(x))
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x,dim=1)



'''
Second model, multiclasses classifier(log softmax at the end)
NN with 2 hidden layers using relu as
activation function and Dropout on the output of the relu.
Dropout lowers the overfit, reduce dependency between hidden neuornons.
'''
class B(nn.Module):

    def __init__(self, image_size, FL, SL):
        super(B, self).__init__()
        self.image_size = image_size
        self.fc0 = nn.Linear(image_size, FL)
        self.fc1 = nn.Linear(FL, SL)
        self.fc2 = nn.Linear(SL, 10)

    def forward(self, x):
        x = x.view(-1, self.image_size)
        x = F.relu(self.fc0(x))
        x = F.dropout(x, training=self.training)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)



'''
Third model, multiclasses classifier(log softmax at the end)
NN with 2 hidden layers using relu as
activation function and batch-norm on the hidden layers
what helps convergance rate and reduce problems like internal covariate shift.
'''
class C(nn.Module):

    def __init__(self, image_size, FL, SL):

        super(C, self).__init__()
        self.image_size = image_size
        self.fc0 = nn.Linear(image_size, FL)
        self.fc1 = nn.Linear(FL, SL)
        self.fc2  = nn.Linear(SL, 10)
        self.bn1 = nn.BatchNorm1d(FL)
        self.bn2 = nn.BatchNorm1d(SL)



    def forward(self, x):
        x = x.view(-1, self.image_size)
        x = self.bn1(F.relu(self.fc0(x)))
        x = self.bn2(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)







'''
making test global so i can use it in test function.
'''
test = datasets.FashionMNIST(root='./data',
                                  train=False,
                                  transform=transforms.ToTensor())

testSet = torch.utils.data.DataLoader(dataset=test,
                                      batch_size=1,
                                      shuffle=False)
'''
Main gets Runs one of the models:
'''
def main():

    '''
    Defining Parameters:
    '''
    print "Creating Parameters and Getting Data...\n\n"
    #hyper and regular:
    epoches = 10;
    LearningRate = 0.001;
    batch_size=64
    FirstLayer = 100;
    SecondLayer = 50;
    NumOfPixels = 784;

    #model and optimizer:
    myModel=B(image_size=NumOfPixels,FL=FirstLayer,SL=SecondLayer)
    myOptimizer=optim.Adam(myModel.parameters(),lr=LearningRate)





    '''
    Getting the Data and Splitting it, THIS CODE WAS TAKEN FROM YOUR LINK IN THE EXCERSICE.
    '''

    train = datasets.FashionMNIST(root='./data',
                                   train=True,
                                   transform=transforms.ToTensor(),
                                   download=True)

    # Splitting:

    #validation set:
    precentageOFcut=0.2
    ind = list(range(len(train)))
    split = int(len(train)*precentageOFcut)
    valCut = np.random.choice(ind, size=split, replace=False)
    samplerVal = SubsetRandomSampler(valCut)
    validationSet = torch.utils.data.DataLoader(dataset=train,
                                                    batch_size=1, sampler=samplerVal)

    #train set:
    trainCut = list(set(ind) - set(valCut))
    samplerT = SubsetRandomSampler(trainCut)
    trainSet = torch.utils.data.DataLoader(dataset=train,
                                               batch_size=batch_size, sampler=samplerT)


    '''
    Now, the interesting part
    Train and Test:
    '''
    print "Training Starts: ..\n\n"

    trainModel(myModel,epoches,myOptimizer,trainSet,validationSet,batch_size)


    return 0;


'''
Train the model and print results.
I used the algorithem from the piazza->pytorch version of NN.
'''

def trainModel(myModel, epoches, myOptimizer, TrainSet, ValSet, bSize):

    myModel.train()

    #creating dictionaries for graph
    training_exapleAndPred = dict()
    validation_exampleAndPred = dict()

    #train:
    for i in range(1,epoches+1):
        print "Epoch Number :" + str(i)

        for example, lable in TrainSet :
            myOptimizer.zero_grad()
            #getting the ytag of model
            output = myModel(example)
            #calc loss
            loss = F.nll_loss(output, lable)
            #back-prop
            loss.backward()
            #update parameters..
            myOptimizer.step()


        #adding results to later plot graph...
        setName="TrainSet"
        TrainLoss = getResults(TrainSet,setName , myModel, bSize)
        training_exapleAndPred[i] = TrainLoss

        setName="ValidationSet"
        ValLoss = getResults(ValSet,setName, myModel, 1)
        validation_exampleAndPred[i] = ValLoss

    #plot results:
    printGraph(training_exapleAndPred,validation_exampleAndPred)

    #applying test
    test(myModel)



    return 0;

'''
Testing the model and writing the prediction file,
the code is similar to the getResults function.

USED THE CODE FROM TIRGUL.
'''
def test(myModal):
    #getting ready for test:
    print "\n\nTest time :...\n"
    pred_file = open("test.pred", 'w')
    myModal.eval()
    test_loss = 0
    correct = 0

    #testing:
    for data, target in testSet:
        output = myModal(data)
        test_loss += F.nll_loss(output, target, size_average=False).item()  # sum up batch loss
        pred = output.data.max(1, keepdim=True)[1]  # get the index of the max log-probability
        pred_file.write(str(pred.item()) + "\n")
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()
    test_loss /= len(testSet.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(testSet.dataset),
        100. * correct / len(testSet.dataset)))


    pred_file.close()

    return 0;


'''
check Results on each set, USED THE CODE FROM TIRGUL.
'''
def getResults(Set,SetName,Mymodel,bSize):
    Mymodel.eval()
    loss = 0
    modelWasRight = 0

    #predict and compare to real
    for example, lable in Set:
        output = Mymodel(example)
        loss += F.nll_loss(output, lable, size_average=False).item()  # sum up batch loss
        pred = output.data.max(1, keepdim=True)[1]                    # get the index of the max log-probability
        modelWasRight += pred.eq(lable.data.view_as(pred)).cpu().sum()


    #calc loss and print results:
    loss /= (len(Set)*bSize)
    print('\n'+SetName+': Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        loss, modelWasRight, (len(Set)*bSize),
        100. * modelWasRight / (len(Set)*bSize)))
    return loss


'''
Plot graph for each set.
'''
def printGraph(training_exapleAndPred,validation_exampleAndPred ):

    #plot the results
    label1, = plt.plot(training_exapleAndPred.keys(), training_exapleAndPred.values()
                       , "g-", label='TrainingSet loss')

    label2, = plt.plot(validation_exampleAndPred.keys(),
                       validation_exampleAndPred.values(), "b-", label='validationSet loss')
    plt.legend(handler_map={label2: HandlerLine2D(numpoints=2)})
    plt.show()


    return 0;




if __name__ == "__main__":
    main()