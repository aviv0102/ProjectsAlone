'''
Aviv Shisman 206558157    Itay Hassid 209127596
'''
import sys
import liblin as linear
import ExtractFeatures

#global:
inputName = sys.argv[1]            #input
modelName = sys.argv[2]            #model we trained file name
featureMapName = sys.argv[3]       #map from feature to feature index
outName = sys.argv[4]              #output
featureMap={}
tagDict={}

'''
main
'''
def main():
    #train:
    print "Hello! Your in Greedy MaxEnt, Please Wait a moment while we load...\n\n"
    print "Starting! it might take few seconds\n"
    read()
    print "Files are ready, u can remove the comment from percentage function for %acc"



# reading file and creating output
def read():
    readMap()
    tags=readInput()
   # precentage(tags)

    return

'''
main loop
'''
def readInput():
    libl=linear.LiblinearLogregPredictor(modelName)
    f = open(inputName, 'r')
    output=open(outName,'w')
    y = []
    for line in f.readlines():
        words = line.rstrip().split(' ')
        i=0
        pt='start'
        ppt='start'
        for word in words:
            features=ExtractFeatures.Extract(word,'','',i,words)
           # features.append(('pt',pt))
           # features.append(('ppt',ppt))
            vec=ToVectorNums(features)

            y_hat = predict(vec,word, libl)
            y.append(y_hat)
            ppt=pt
            pt=y_hat
            i+=1
            output.write(word+'/'+y_hat+' ') #updating answer file!
        output.write('\n')


    return y

'''
predict...
'''
def predict(vec, word, libl):

    max_prob = 0.0
    max_label = "NN"

    probs = libl.predict(vec,0)

    for index, prob in probs.iteritems():
        if prob > max_prob:
            max_prob = prob
            max_label = str(tagDict[index])
    return max_label

'''
turning input (words) to format that the model can predict(liblinear format)
'''
def ToVectorNums(features_line):
    vec = []
    for feature in features_line:
        if featureMap.has_key(feature):
            vec.append(int(featureMap[feature]))

    vec = list(reversed(sorted(vec)))
    vec.append(int(0))
    return list(reversed(vec))

'''
getting map from file
'''
def readMap():
    mapIn=open(featureMapName,'r')
    for line in mapIn.readlines():
        if line.startswith('*'):
            continue
        tokens = line.rstrip().split(' ')
        token=tokens[0].rsplit('=', 1)
        key=token[0]
        value=token[1]
        index=tokens[1]
        if key == 'tag':
            tagDict[index]=value
        else:
            featureMap[(key,value)]=index


'''
Checking how good the model is
'''
def precentage(OurTags):
    correct=0
    sumTillNow=0
    TestCheck = 'ass1-tagger-test'  # added for % accuracy
    f = open(TestCheck, 'r')
    for line in f.readlines():
        words = line.rstrip().split(' ')
        for i in range(len(words)):
            sp = words[i].rsplit('/', 1)
            y= sp[1]
            y_tag = OurTags[sumTillNow]
            sumTillNow+=1
            if y==y_tag:
                correct+=1
    print('\nTest set: Accuracy: {}/{} ({:.0f}%)\n'.format(
        correct,sumTillNow,
        100. * correct / sumTillNow))










if __name__ == "__main__":
    main()
