'''
Aviv Shisman 206558157  Itay Hassid 209127596
'''

#imports:
import sys


'''
Our program find the 'Live_in' relations in a corpus
'''
def main():

    print('Hello! we will now calculate recall,precision,f1 score')

    if len(sys.argv)!=3:
        print('Error!')
        print('Please insert the following arguments:')
        print('1 - the result.txt that was the output from extract.py')
        print('2 - the dev annotations for evaluation')
        return

    print('results:\n')
    f1(sys.argv[1],sys.argv[2])


'''
calculate f1,recall,precision
'''
def f1(ourPredFile,testPredName):
    pred = []
    gold = []
    f = open(testPredName, 'r')
    g = open(ourPredFile, 'r')
    # getting the relations of gold standard
    for line in f.readlines():
        splited = line.rstrip('\n').split('\t')
        if splited[2] == 'Live_In':
            annot = tuple(splited[:4])
            gold.append(annot)

    for line in g.readlines():
        splited = line.rstrip('\n').split('\t')
        if splited[2] == 'Live_In':
            annot = tuple(splited[:4])
            pred.append(annot)

    g.close()
    f.close()

    # calculate true and false positive
    truePositive = 0
    falsePostive=0
    for example in pred:
        if example in gold:
            truePositive += 1
        else:
            falsePostive+=1


    # calculate false negative (no need to filter...)
    falseNeg=0
    for e in gold:
        if not e in pred:
            falseNeg+=1


    recall = 1.0*truePositive/(truePositive+falseNeg)
    precision = 1.0*truePositive/(truePositive+falsePostive)
    f1_score = 2*((precision*recall)/(precision+recall))
    print('recall=', recall, ', precision= ',
          precision, ', f1= ', f1_score)

if __name__ == '__main__':
    main()
