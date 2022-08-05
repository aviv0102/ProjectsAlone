'''
name: Aviv shisman
id:   206558157
'''

#imports:
import torch
from torchvision import datasets, transforms,models
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.sampler import SubsetRandomSampler
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from sklearn.metrics import confusion_matrix






'''
Main gets Runs one of the models:
'''
def main():

    '''
    Defining Parameters:
    '''
    print "Creating Parameters and Getting Data...\n\n"
    #hyper and regular:
    epoches = 1;
    LearningRate = 0.001;
    batch_size=64

    #model and optimizer:

    myModel = models.resnet18(pretrained=True)
    for param in myModel.parameters():
        param.requires_grad = False

    # Parameters of newly constructed modules have requires_grad=True by default
    num_ftrs =myModel.fc.in_features
    myModel.fc = nn.Linear(num_ftrs, 10)
    myOptimizer=optim.Adam(myModel.fc.parameters(),lr=LearningRate)
    criterion = nn.CrossEntropyLoss()




    '''
    Getting the Data and Splitting it, THIS CODE WAS TAKEN FROM YOUR LINK IN THE EXCERSICE.
    '''
    print"getting train set for Resnet\n\n"

    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    train =  datasets.CIFAR10(root='./data',
                                          train=True,
                                          transform=transforms.Compose([transforms.Resize(224),
                                                                       transforms.ToTensor()]),

                                          download=True)

    print "\ngetting test\n"


    test = datasets.CIFAR10(root='./data',
                                         train=False,
                                         transform=transforms.Compose([transforms.Resize(224),
                                                                       transforms.ToTensor()]))

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

    trainModel(myModel,epoches,myOptimizer,trainSet,validationSet,batch_size,testSet,criterion)


    return 0;


'''
Train the model and print results.
I used the algorithem from the piazza->pytorch version of NN.
'''

def trainModel(myModel, epoches, myOptimizer, TrainSet, ValSet, bSize,ts,cr):

    myModel.train()

    #creating dictionaries for graph
    training_exapleAndPred = dict()
    validation_exampleAndPred = dict()

    #train:
    for i in range(1,epoches+1):
        print "Epoch Number :" + str(i)
        print "start epoch\n"
        for example, lable in TrainSet :
            myOptimizer.zero_grad()
            #getting the ytag of model
            output = myModel(example)
            #calc loss
            loss = cr(output, lable)
            #back-prop
            loss.backward()
            #update parameters..
            myOptimizer.step()
        print "train end\n"

        #adding results to later plot graph...
        print "Train Loss start\n"
        setName="TrainSet"
        TrainLoss = getResults(TrainSet,setName , myModel, bSize,cr)
        training_exapleAndPred[i] = TrainLoss
        print "Train Loss end\n\n"

        print "validation Loss start\n"
        setName="ValidationSet"
        ValLoss = getResults(ValSet,setName, myModel, 1,cr)
        validation_exampleAndPred[i] = ValLoss
        print "Validation Loss end\n\n"

    #plot results:
    print "print results\n"
    printGraph(training_exapleAndPred,validation_exampleAndPred)

    #applying test


    test(myModel,ts,cr)



    return 0;

'''
Testing the model and writing the prediction file,
the code is similar to the getResults function.

USED THE CODE FROM TIRGUL.
'''
def test(myModal,testSet,cr):
    #getting ready for test:
    print "\n\nTest time :...\n"
    pred_file = open("ResnetTest.pred", 'w')
    myModal.eval()
    test_loss = 0
    correct = 0
    y_tag = []
    y_pred = []

    #testing:
    for data, target in testSet:
        output = myModal(data)
        test_loss += cr(output, target)  # sum up batch loss
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
check Results on each set, USED THE CODE FROM TIRGUL.
'''
def getResults(Set,SetName,Mymodel,bSize,cr):
    Mymodel.eval()
    loss = 0
    modelWasRight = 0

    #predict and compare to real
    for example, lable in Set:
        output = Mymodel(example)
        loss += cr(output, lable)  # sum up batch loss
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