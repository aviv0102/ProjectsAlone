'''
Aviv Shisman 206558157  Itay Hassid 209127596
'''
import sys

inputName = sys.argv[1] #test
qName = sys.argv[2] #q.mle name
eName = sys.argv[3] #e.mle name
answerFileName= sys.argv[4] #answer file name


TestCheck='ass1-tagger-test'#added for % accuracy


#global dictionaries
num_of_tags = {}  # how much each tag {tag: num}
dictNameTag = {}  # {(name,tag):num}
dictSignatureTag = {} # {(signature, tag):num}
dictTagTag = {}  # counting (tag,tag) (tag,tag,tag) appearances
num_of_words = 0  # all words in document



'''
Main!
'''
def main():
    #train:
    print "Hello! Please Wait a moment while we load...\n\n"
    uploadQ()
    uploadE()
    print "Starting!\n"
    greedy()

    print "Answer File is Ready!"


'''
Prediction algorithem
'''
def greedy():
    f = open(inputName, 'r')
    answerFile = open(answerFileName, 'w')
    scoringTag = []
    for line in f.readlines():
        words = line.rstrip().split(' ')
        possibleTags=num_of_tags.keys()
        MaxTag = ['', -1]
        for i in range(len(words)):
            MaxTag[1] = -1
            current=['', -1]
            isWordAppeared = False
            for tag in possibleTags:
                if i == 0:
                    current[1]= getE(words[i],tag)*getQ('start', 'start', tag)
                    current[0]=tag
                elif i == 1:
                    current[1]= getE(words[i], tag) * getQ('start', scoringTag[i-1], tag)
                    current[0]=tag
                else:
                    current[1] = getE(words[i], tag) * getQ(scoringTag[i-2], scoringTag[i - 1], tag)
                    current[0] = tag

                if current[1] != 0: # getE * getQ != 0
                    isWordAppeared = True
                if(MaxTag[1] < current[1]):
                    MaxTag[0] = tag
                    MaxTag[1] = current[1]
            if isWordAppeared == False:
                MaxTag[0] = getSignatures(words[i])
            scoringTag.append(MaxTag[0])
            answerFile.write(words[i]+"/"+MaxTag[0]+' ')
        answerFile.write('\n')
    precentage(scoringTag)
    #precentage(scoringTag)
'''
Check if Value exists if it does increase the val by 1, else: create new entery
'''
def checkExist(myDict, arg1, arg2, arg3=''):
    if arg3=='':
        if myDict.has_key((arg1, arg2)):
            myDict[(arg1, arg2)] += 1
        else:
            myDict[(arg1, arg2)] = 1

    else:
        if myDict.has_key((arg1, arg2, arg3)):
            myDict[(arg1, arg2,arg3)] += 1
        else:
            myDict[(arg1, arg2, arg3)] = 1


'''
Upload Q from file
'''
def uploadQ():

    qFile = open(qName, 'r')

    for line in qFile.readlines():
        words = line.rstrip().split('\t')
        keysTogether=words[0]
        keys=keysTogether.split(' ')
        value=words[1]
        if len(keys)>2:
            dictTagTag[(keys[0],keys[1],keys[2])]=int(value)
        else:
            dictTagTag[(keys[0],keys[1])]=int(value)

    qFile.close()



'''
Signatures for unFamiliar words
'''
def getSignatures(name):
    try:
        eval(name)
        return 'CD'
    except:
        pass
    st = str(name)
    if st[0].isupper():
        word = '^A'
    elif st.endswith('ing'):
        word = '^ing'
    elif st.endswith('ed'):
        word = '^ed'
    elif st.endswith('ies'):
        word = '^ies'
    elif st.endswith('es'):
        word = '^es'
    elif st.startswith('un'):
        word = '^un'
    elif st.startswith('non'):
        word = '^non'
    elif st.startswith('im'):
        word = '^im'
    else:
        word = '^UNK'
    maxNum = 0
    maxTag = ''
    possible_tags = num_of_tags.keys()
    for tag in possible_tags:
        if dictSignatureTag.has_key((word, tag)):
            if dictSignatureTag[(word, tag)] > maxNum:
                maxNum = dictSignatureTag[(word, tag)]
                maxTag = tag
    return maxTag






'''
Upload E from file
'''
def uploadE():

    eFile = open(eName, 'r')
    global num_of_words
    for line in eFile.readlines():
        words = line.rstrip().split('\t')
        keysTogether=words[0]
        keys=keysTogether.split(' ')
        value=words[1]
        if len(keys)>1:
            if keys[0].startswith('^'):
                dictSignatureTag[(keys[0],keys[1])]=int(value)
            else:
                dictNameTag[(keys[0],keys[1])]=int(value)
                num_of_words+=1
        else:
            num_of_tags[keys[0]]=int(value)
    eFile.close()


'''
calc Q
'''
def getQ(t1, t2, tag):
    lam=[0.7, 0.2, 0.1]
    try:
        first = lam[0]*(dictTagTag[(t1, t2, tag)] * 1.0 / dictTagTag[(t1, t2)])
    except KeyError:
        first = 0
    try:
        second = lam[1]*(dictTagTag[(t2, tag)] * 1.0 / num_of_tags[t2])
    except KeyError:
        second = 0
    try:
        third = lam[2] *(num_of_tags[tag] * 1.0 / num_of_words)
    except KeyError:
        third = 0
    return first + second + third


'''
calc E
'''
def getE(name, tag):
    if dictNameTag.has_key((name, tag)):
        if num_of_tags.has_key(tag):
            return dictNameTag[(name, tag)]*1.0 / num_of_tags[tag]
        else:
            print 'error'
    return 0



'''
get % acc
'''
def precentage(OurTags):
    correct=0
    sumTillNow=0
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
