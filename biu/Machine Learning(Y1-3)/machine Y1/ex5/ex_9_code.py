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
from sklearn.metrics import confusion_matrix


'''
First Model,CNN on CIFAR-10 dataset
I applied Batch-norm for faster convergance rate and to prevent problems (like internal covariate shift)
and Droput to reduce overfitting.

My activation function was Relu and i used 2 Conv layers for the CNN.
'''
class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.image_size=5*5*100;
        self.fc0 = nn.Linear(5*5*100, 100)
        self.fc1 = nn.Linear(100, 50)
        self.fc2 = nn.Linear(50, 10)
        self.conv1 = nn.Conv2d(3, 50, 5)
        self.conv2 = nn.Conv2d(50, 100, 5)
        self.batchN1 = nn.BatchNorm1d(100)
        self.batchN2 = nn.BatchNorm1d(50)

    def forward(self, x):
        x= F.relu(self.conv1(x))
        x = F.max_pool2d(x,(2,2))
        x = F.dropout2d(x, 0.4)

        x=  F.relu(self.conv2(x))
        x = F.max_pool2d(x,(2,2))
        x = F.dropout2d(x, 0.4)


        x = x.view(-1, self.image_size)
        x = F.relu(self.batchN1(self.fc0(x)))
        x = F.dropout(x, 0.4)
        x = F.relu(self.batchN2(self.fc1(x)))
        x = F.dropout(x,0.4)

        x = self.fc2(x)
        return F.log_softmax(x, dim=1)





'''
Main - I USED THE SAME CODE FROM LAST EXERCISE AS BASE.
'''
def main():

    '''
    Defining Parameters:
    '''
    print "Creating Parameters and Getting Data...\n\n"
    #hyper and regular:
    epoches =5;
    LearningRate = 0.0005;
    batch_size=100;

    #model and optimizer:
    myModel=ConvNet()
    myOptimizer=optim.Adam(myModel.parameters(),lr=LearningRate)




    '''
    Getting the Data and Splitting it, THIS CODE WAS TAKEN FROM YOUR LINK IN THE EXCERSICE.
    '''
    print"getting train set\n\n"

    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    train = datasets.CIFAR10(root='./data',
                                          train=True,
                                          transform=transform,
                                          download=True)

    print "\ngetting test\n"


    test = datasets.CIFAR10(root='./data',
                                         train=False,
                                         transform=transform)

    testSet = torch.utils.data.DataLoader(dataset=test,
                                          batch_size=1,
                                          shuffle=False)
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

    trainModel(myModel,epoches,myOptimizer,trainSet,validationSet,batch_size,testSet)


    return 0;


'''
Train the model and print results.
I used the code and functions from last Exercise.
'''

def trainModel(myModel, epoches, myOptimizer, TrainSet, ValSet, bSize,ts):

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


    test(myModel,ts)



    return 0;

'''
Testing the model and writing the prediction file,
the code is similar to the getResults function.
'''
def test(myModal,testSet):
    #getting ready for test:
    print "\n\nTest time :...\n"
    pred_file = open("test.pred", 'w')
    myModal.eval()
    test_loss = 0
    correct = 0
    y_tag = []
    y_pred = []

    #testing:
    for data, target in testSet:
        output = myModal(data)
        test_loss += F.nll_loss(output, target, size_average=False).item()  # sum up batch loss
        pred = output.data.max(1, keepdim=True)[1]  # get the index of the max log-probability
        y_tag.append(target.item())
        y_pred.append(pred.item())
        pred_file.write(str(pred.item()) + "\n")
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()
    test_loss /= len(testSet.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(testSet.dataset),
        100. * correct / len(testSet.dataset)))

    # create matrix
    confusion_mat = confusion_matrix(y_tag, y_pred)
    print(confusion_mat)


    pred_file.close()

    return 0;


'''
check Results on each set
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