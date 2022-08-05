'''
Aviv Shisman 206558157    Itay Hassid 209127596
'''
import sys


#global:
inputName = sys.argv[1]            #input
FeaturesFileName = sys.argv[2]     #output


'''
main
'''
def main():
    #train:
    print "Hello Your are in Extract! Please Wait a moment while we load...\n\n"
    print "Starting! it might take few seconds\n"
    read()

    print "Files are ready for next stage!"


# reading file and creating output
def read():
    f = open(inputName, 'r')
    output = open(FeaturesFileName, 'w')
    for line in f.readlines():
        words = line.rstrip().split(' ')
        i=0
        for token in words:
            sp = token.rsplit('/', 1)
            word = sp[0]
            tag = sp[1]
            Extract(word,tag,output,i,words)
            i += 1

    output.close()
    f.close()

def Extract(word,tag,output,i,words):

    features=[]

    # tag
    if output!='':
        output.write('tag=' + tag + ' ')

    # form
    if output!='':
        output.write('form=' + word + ' ')
    features.append(('form',word))


    # get known signature
    sig = getSignatures(word)
    if output != '':
        output.write('sig=' + sig + ' ')
    features.append(('sig', sig))

    # check if there is ending with 3 characters (more sigs)
    ending = check3end(word)
    if ending != "none":
        if output != '':
            output.write('3suff=' + ending + ' ')
        features.append(('3suff', ending))

    # check if there is ending with 2 characters(more sigs)
    ending = check2end(tag)
    if ending != "none":
        if output != '':
            output.write('2suff=' + ending + ' ')
        features.append(('2suff', ending))


    # prev word
    if i > 0:
        if output != '':
            prevWord =words[i - 1].rsplit('/', 1)
            output.write('pw=' + prevWord[0] + ' ')

        features.append(('pw', words[i-1]))

    # prev prev word
    if i > 1:
        ppW = words[i - 2].rsplit('/', 1)
        prevprevWord = ppW[0]
        if output != '':
            output.write('ppw=' + prevprevWord + ' ')
        features.append(('ppw', words[i-2]))


    last=len(words)-1
    secondLast=len(words)-2

    if i<secondLast:
        if output != '':
            nextword = words[i + 1].rsplit('/', 1)
            nextnextWord=words[i +2].rsplit('/', 1)
            output.write('nw=' + nextword[0] + ' ')
            output.write('nnw=' + nextnextWord[0] + ' ')
        features.append(('nw', words[i + 1]))
        features.append(('nnw', words[i + 2]))
    elif i<last:
        if output != '':
            nextword = words[i + 1].rsplit('/', 1)
            output.write('nw=' + nextword[0] + ' ')
            output.write('nnw=' +'end ')
        features.append(('nw', words[i + 1]))
        features.append(('nnw','end'))
    else:
        if output != '':
            output.write('nw=' + 'end')
            output.write('nnw=' +'end ')
        features.append(('nw', 'end'))
        features.append(('nnw','end'))


    # prev tag
    if i > 0:
        if output != '':
            prevWord = words[i - 1].rsplit('/', 1)
            prevtag = prevWord[1]
            output.write('pt=' + prevtag + ' ')
    else:
        if output != '':
            output.write('pt=start ')

    # prev prev tag
    if i > 1:
        if output != '':
            prevprevWord = words[i - 2].rsplit('/', 1)
            prevprevtag = prevprevWord[1]
            output.write('ppt=' + prevprevtag + ' ')
    else:
        if output != '':
            output.write('ppt=start ')

    if output!='':
        output.write("\n")

    return features




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

def check3end(word):
    ending = word[-3:]

    if ending == "ing":
        return ending
    if ending == "ies":
        return ending
    if ending == "ate":
        return ending
    if ending == "ify":
        return ending
    if ending == "ise":
        return ending
    if ending == "ize":
        return ending
    if ending == "ful":
        return ending
    if ending == "ous":
        return ending
    if ending == "ism":
        return ending
    if ending == "ist":
        return ending
    if ending == "ity":
        return ending
    if ending == "ish":
        return ending
    if ending == "ive":
        return ending
    if ending == "acy":
        return ending
    if ending == "dom":
        return ending

    return "none"

def check2end(word):
    ending = word[-2:]

    if ending == "ed":
        return ending
    if ending == "es":
        return ending
    if ending == "ic":
        return ending
    if ending == "ly":
        return ending
    if ending == "al":
        return ending
    if ending == "er":
        return ending
    if ending == "or":
        return ending
    if ending == "ty":
        return ending
    if ending == "en":
        return ending
    return "none"

if __name__ == "__main__":
    main()
