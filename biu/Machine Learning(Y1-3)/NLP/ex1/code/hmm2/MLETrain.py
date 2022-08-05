'''
Aviv Shisman 206558157  Itay Hassid 209127596
'''
import sys


#global:
inputName = sys.argv[1]
qName = sys.argv[2]
eName = sys.argv[3]
num_of_tags = {}  # how much each tag
dictNameTag = {}  # {(name,tag):num}
dictSignatureTag = {} #signaturesDict


'''
Main
'''
def main():
    #train:
    print "Hello!This is HMM Training. Please Wait a moment while we load..."
    print "Starting!"
    eCount()
    qCount()

    print "Files are ready!"

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
Signatures for unFamiliar words
'''
def setSignatures(name, tag):
    try:
        float(name)
        num_of_tags['CD'] += 1
        checkExist(dictSignatureTag, '^num', 'CD', '')
    except ValueError:
        pass
    st = str(name)
    if st.endswith('ing'):
        checkExist(dictSignatureTag, '^ing', tag, '')
    elif st.isupper():
        checkExist(dictSignatureTag, '^AAA', tag, '')
    elif st.istitle():
        checkExist(dictSignatureTag, '^A', tag, '')
    elif st.endswith('ed'):
        checkExist(dictSignatureTag, '^ed', tag, '')
    elif st.endswith('ies'):
        checkExist(dictSignatureTag, '^ies', tag, '')
    elif st.endswith('es'):
        checkExist(dictSignatureTag, '^es', tag, '')
    elif st.endswith('ly'):
        checkExist(dictSignatureTag, '^ly', tag, '')
    elif st.endswith('er'):
        checkExist(dictSignatureTag, '^er', tag, '')
    elif st.startswith('un'):
        checkExist(dictSignatureTag, '^un', tag, '')
    elif st.startswith('anti'):
        checkExist(dictSignatureTag, '^anti', tag, '')
    elif st.startswith('inter'):
        checkExist(dictSignatureTag, '^inter', tag, '')
    elif st.startswith('de'):
        checkExist(dictSignatureTag, '^de', tag, '')
    elif st.startswith('an'):
        checkExist(dictSignatureTag, '^an', tag, '')
    elif st.startswith('abs'):
        checkExist(dictSignatureTag, '^abs', tag, '')
    elif st.startswith('ab'):
        checkExist(dictSignatureTag, '^ab', tag, '')
    elif st.startswith('dis'):
        checkExist(dictSignatureTag, '^dis', tag, '')
    elif st.startswith('im'):
        checkExist(dictSignatureTag, '^im', tag, '')
    elif st.startswith('in'):
        checkExist(dictSignatureTag, '^in', tag, '')
    elif st.startswith('non'):
        checkExist(dictSignatureTag, '^non', tag, '')
    elif st.endswith('s'):
        checkExist(dictSignatureTag, '^s', tag, '')
    elif st.startswith('a'):
        checkExist(dictSignatureTag, '^a', tag, '')
    elif any(x == '-' for x in st):
        checkExist(dictSignatureTag, '^-', tag, '')
    elif any(not x.isalpha() for x in st):
        checkExist(dictSignatureTag, '^$', tag, '')
    else:
        checkExist(dictSignatureTag, '^UNK', tag, '')


'''
Count for q.mle
'''
def qCount():

    dictTagTag = {('start', 'start'): 0, ('start'): 0}  # counting (tag,tag) (tag,tag,tag) appearances
    f = open(inputName, 'r')
    qFile = open(qName, 'w')

    # creating q.mle file. (Tag, Tag [,Tag])
    for line in f.readlines():
        words = line.rstrip().split(' ')
        arr = []
        dictTagTag[('start', 'start')] += 1
        dictTagTag[('start')] += 1
        for i in range(len(words)):
            # print(word)
            sp = words[i].rsplit('/', 1)
            arg2 = sp[1]
            arr.append(arg2)

        for i in range(len(arr)):
            if i == 0:
                checkExist(dictTagTag, "start", "start", arr[0])
                checkExist(dictTagTag, "start", arr[0])
            elif i == 1:
                checkExist(dictTagTag, "start", arr[0], arr[1])
                checkExist(dictTagTag, arr[0], arr[1])
            else:
                checkExist(dictTagTag, arr[i - 2], arr[i - 1], arr[i])
                checkExist(dictTagTag, arr[i - 1], arr[i])
    f.close()
    for key, value in dictTagTag.iteritems(): # python2.7 : d.iteritems()
        qFile.write(' '.join(key) + '\t' + str(value) + '\n')
    qFile.close()

'''
Count for e.mle
'''
def eCount():

    f = open(inputName, 'r')
    eFile = open(eName, 'w')
    i=0
    for line in f.readlines():
        words = line.rstrip().split(' ')
        for word in words:
            sp = word.rsplit('/', 1)
            arg1 = sp[0]
            arg2 = sp[1]
            # counting Tags types
            if arg2 in num_of_tags.keys():
                num_of_tags[arg2] += 1
            else:
                num_of_tags[arg2] = 1

            #counting (name,tag:value)
            if dictNameTag.has_key((arg1, arg2)):
                dictNameTag[(arg1, arg2)] += 1
                setSignatures(arg1,arg2)
            else:
                dictNameTag[(arg1, arg2)] = 1
                setSignatures(arg1,arg2)


    for key, value in dictNameTag.items(): # Writing name,tag dictionary
        eFile.write(' '.join(key) + '\t' + str(value) + '\n')

    for key, value in num_of_tags.items(): # Writing TagTypesDictioary
        eFile.write(key + '\t' + str(value) + '\n')

    for key, value in dictSignatureTag.items(): # Writing SignaturesDictionary
        eFile.write(' '.join(key) + '\t' + str(value) + '\n')

    eFile.close()
    f.close()




if __name__ == "__main__":
    main()
