'''
Aviv Shisman 206558157  Itay Hassid 209127596
'''
import sys
import numpy as np
import math


inputName = sys.argv[1] #test
qName = sys.argv[2] #q.mle name
eName = sys.argv[3] #e.mle name
answerFile= sys.argv[4] #answer file name


TestCheck='ass1-tagger-test'#added for % accuracy


#global dictionaries
num_of_tags = {}  # how much each tag {tag: num}
dictNameTag = {}  # {(name,tag):num}
dictSignatureTag = {} # {(signature, tag):num}
dictTagTag = {}  # counting (tag,tag) (tag,tag,tag) appearances
num_of_words = 0  # all words in document
wordsList = set() #for viterbi
dictAvailibleTags = {}  # {name: tags (list) }

'''
Main!
'''
def main():
    #train:
    print "Hello! Please Wait a moment while we load..."
    uploadQ()
    uploadE()
    availibleTags()
    print "Starting!"
    HMM()

    print "Answer File is Ready!"


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
    # elif st.startswith('a'):
    #     word = '^a'
    elif any(x == '-' for x in st):
        return "^-"
    elif any(not x.isalpha() for x in st):
        return "^$"
    else:
        word = '^UNK'

    return word

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
    if dictSignatureTag.has_key((name, tag)):
        if num_of_tags.has_key(tag):
            return dictSignatureTag[(name, tag)]*1.0 / num_of_tags[tag]
        else:
            print 'error'
    return 0


'''
get Available tags
'''
def availibleTags():
    for key in dictNameTag.keys():
        if dictAvailibleTags.has_key(key[0]):
            dictAvailibleTags[key[0]].append(key[1])
        else:
            dictAvailibleTags[key[0]] = [key[1]]
    for key in dictSignatureTag.keys():
        if dictAvailibleTags.has_key(key[0]):
            dictAvailibleTags[key[0]].append(key[1])
        else:
            dictAvailibleTags[key[0]] = [key[1]]
'''
HMM
'''
def HMM():
    f = open(inputName, 'r')
    ans= open('answer','w')
    scoringTag = []
    countLine = 0
    for line in f.readlines():
        words = line.rstrip().split(' ')
        newTags = viterbi(words)
        countLine += 1
        scoringTag.extend(newTags)
        for i in range (len(newTags)):
            st=str(newTags[i])
            ans.write(words[i]+"/"+st+' ')
        ans.write('\n')
    f.close()
    ans.close()
   # precentage(scoringTag)

'''
Viterbi Algorithem With BackPointers and Modifications for speed
'''
def viterbi(words):
        v = [{("start", "start"): 0.0}]
        bp = []
        for i, word in enumerate(words):

            if not word in dictAvailibleTags:
                word = getSignatures(word)

            max_prob = {}
            max_tags = {}
            for t_tag, t in v[i]:
                available_tags = dictAvailibleTags[word]
                for r in available_tags:
                    prob = getScore(word, r, t, t_tag)
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
        # print list(reversed(y))
        return list(reversed(y))

'''
get score of tag
'''
def getScore(word, tag, prev_tag, prev_prev_tag):
    q = getQ(prev_prev_tag, prev_tag, tag)
    e = getE(word, tag)
    if not (e == 0 or q == 0):
        prob = math.log(e) + math.log(q)
    else:
        prob = float("-inf")
    return prob

'''
Checking Accuracy
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
    f.close()
    print('\nTest set: Accuracy: {}/{} ({:.0f}%)\n'.format(
        correct,sumTillNow,
        100. * correct / sumTillNow))

if __name__ == "__main__":
    main()
