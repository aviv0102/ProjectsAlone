'''
Aviv Shisman 206558157    Itay Hassid 209127596
'''
import sys
import liblin as linear
import ExtractFeatures
import math

#global:
inputName = sys.argv[1]            #input
modelName = sys.argv[2]            #model we trained file name
featureMapName = sys.argv[3]       #map from feature to feature index
outName = sys.argv[4]              #output
featureMap={}
tagDict={}
oppDictTag={}
dictAvailibleTags={}

'''
main
'''
def main():
    #train:
    print "Hello! Your in MEMMTag, Please Wait a moment while we load...\n\n"
    print "Starting! it might take few seconds\n"
    read()

    print "Files are ready for next stage!(you can use per function to get %acc)"


# reading file and creating output
def read():
    readMap()
    tags=MEMM()
    precentage(tags)
    return
'''
Main Loop get sentence and tag it
'''
def MEMM():
    libl=linear.LiblinearLogregPredictor(modelName)
    f = open(inputName, 'r')
    output=open(outName,'w')
    y = []
    for line in f.readlines():
        words = line.rstrip().split(' ')
        i=0
        lineV=[]
        for word in words:
            features=ExtractFeatures.Extract(word,'','',i,words)
            vec=ToVectorNums(features)
            i+=1
            lineV.append(vec)

        yT,y_hat = viterbi(words,lineV, libl)
        y.extend(y_hat)

        #update answer file
        for i in range (len(y_hat)):
            output.write(str(words[i])+'/'+str(y_hat[i])+' ')
        output.write('\n')

    return y

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
reading the map and creating from it dictionaries , each with different role
'''
def readMap():
    mapIn=open(featureMapName,'r')
    for line in mapIn.readlines():

        #for available tags
        if line.startswith('*'):
            token = line.rsplit('=', 1)
            key = token[0]
            value = token[1]
            tempToken = value.rstrip().split('&')
            name = tempToken[0]
            tagsToName = tempToken[1].rstrip().split('#')
            dictAvailibleTags[name] = tagsToName
            continue

        #reading to dictionaries
        tokens = line.rstrip().split(' ')
        token=tokens[0].rsplit('=', 1)
        key=token[0]
        value=token[1]
        index=tokens[1]
        if key == 'tag':
            tagDict[index]=value
            oppDictTag[value]=index
        else:
            featureMap[(key,value)]=index



'''
using viterbi decode to get the best seq of results(following the algorithem with our improvments)
'''
def viterbi(words,LinevVec,libl):
    v = [{("start", "start"): 0}]
    bp = []
    yT=[]
    for i, word in enumerate(words):
        if not word in dictAvailibleTags:
            word = getSignatures(word)
        max_prob = {}
        max_tags = {}
        f=0
        for t_tag, t in v[i]:

            available_tags =dictAvailibleTags[word]
            vec = list(LinevVec[i])
            if featureMap.has_key(('pt', t)):
                vec.append(int(featureMap[('pt', t)]))
            if featureMap.has_key(('ppt', t_tag)):
                vec.append(int(featureMap[('ppt', t_tag)]))

            vec = list(sorted(vec))
            if f==0:
                yT.append(calc(vec, libl))
                f+=1

            prob = max(libl.predict(vec,1))

            for r in available_tags:
                score = v[i][(t_tag, t)] + prob
                if ((t, r) not in max_prob) or score > max_prob[(t, r)]:
                    max_prob[(t, r)] = score
                    max_tags[(t, r)] = t_tag


        v.append(max_prob)
        bp.append(max_tags)

    max_y_end = float("-inf")
    y_n1, y_n = list(v[len(words)].keys())[0]
    for t, r in v[len(words)]:
        y_end = v[len(words)][(t, r)]
        if y_end > max_y_end:
            max_y_end = y_end
            y_n = r
            y_n1 = t
    y = []
    y.append(y_n)
    if len(words) > 1:
        y.append(y_n1)

    prev_t = y_n
    prev_prev_t = y_n1
    for i in xrange(len(v) - 2, 1, -1):
        t = bp[i][(prev_prev_t, prev_t)]
        y.append(t)
        prev_t = prev_prev_t
        prev_prev_t = t

    return list(reversed(y)),yT
'''
help function
'''
def calc(vec, lin):

    temp1 = 0.0
    temp2 = "NN"

    pr = lin.predict(vec,0)

    for index, prPer in pr.iteritems():
        if prPer> temp1:
            temp1 = prPer
            temp2 = str(tagDict[index])
    return temp2

'''
signatures for words we didn't saw before
'''
def getSignatures(name):
    st = str(name)
    try:
        eval(st)
        return '^num'
    except:
        pass
    if st.istitle():
        word = '^A'
    elif st.isupper():
        word = '^AAA'
    elif st.endswith('ing'):
        word = '^ing'
    elif st.endswith('ed'):
        word = '^ed'
    elif st.endswith('ies'):
        word = '^ies'
    elif st.endswith('es'):
        word = '^es'
    elif st.endswith('ly'):
        word = '^ly'
    elif st.endswith('er'):
        word = '^er'
    elif st.startswith('in'):
        word = '^in'
    elif st.startswith('un'):
        word = '^un'
    elif st.startswith('anti'):
        word = '^anti'
    elif st.startswith('inter'):
        word = '^inter'
    elif st.startswith('de'):
        word = '^de'
    elif st.startswith('abs'):
        word = '^abs'
    elif st.startswith('ab'):
        word = '^ab'
    elif st.startswith('dis'):
        word = '^dis'
    elif st.startswith('im'):
        word = '^im'
    elif st.startswith('non'):
        word = '^non'
    elif st.endswith('s'):
        word = '^s'
    elif st.startswith('an'):
        word = '^an'
    elif any(x == '-' for x in st):
        return "^-"
    elif any(not x.isalpha() for x in st):
        return "^$"
    else:
        word = '^UNK'

    return word

'''
for assessing how good is the model(%acc)
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
