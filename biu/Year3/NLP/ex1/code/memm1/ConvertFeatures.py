'''
Aviv Shisman 206558157    Itay Hassid 209127596
'''
import sys
import operator


#global:
inputName = sys.argv[1]              #input
vecFileName = sys.argv[2]           #vecFile output
mapFileName= sys.argv[3]            #map output
featureMap={}
tagMap={}



'''
main
'''
def main():
    #train:
    print "Hello!You are in Convert, Please Wait a moment while we load...\n\n"
    print "Starting! it might take few seconds\n"
    read()

    print "Files are ready for next stage!"

'''
 reading file and creating output(Vectors and Map file)
 Vector file is the features that will be given to the model.
 The map contains:
    -indexing of each feature
    -indexing of each tag 
    -all the available tags for each word/sig(reduce run time)
'''
def read():
    f = open(inputName, 'r')
    outputVec = open(vecFileName, 'w')
    outputMap= open(mapFileName,'w')
    wordCount=1
    tagCount=0
    availableTags = {}
    for line in f.readlines():
        words = line.rstrip().split(' ')
        LineFeatures={} #will be writen every line in ascending order
        i=0
        currentTag=''
        for token in words:
            sp = token.rsplit('=', 1)
            key = sp[0]
            value = sp[1]

            #if it is a tag update the the vec file and map file...
            if key=='tag':
                currentTag=value
                if not tagMap.has_key(value):
                    tagMap[value]=tagCount
                    outputVec.write(str(tagMap[value])+' ')
                    outputMap.write('tag=' + str(value) + ' ' + str(tagCount) + '\n')
                    tagCount+=1
                else:
                    outputVec.write(str(tagMap[value])+' ')

            #else its a word, index it and write it + insert the tag of it in available tags
            else:

                #for available tags...
                if key == 'sig' or key == 'form':
                    if availableTags.has_key(value):
                        availableTags[value].add(currentTag)
                    else:
                        availableTags[value] = {currentTag}

                #indexing the feature in dictionary and writing it (e.g for feature : pw,hello )
                if not featureMap.has_key((key,value)):
                    featureMap[(key, value)] = wordCount
                    LineFeatures[(key,value)] =wordCount #adding it to a dict it will be ordered later by index
                    outputMap.write(str(key) + '=' + str(value) + ' ' + str(wordCount) + '\n')
                    wordCount += 1
                    i+=1

                #the feature was before
                else:
                    LineFeatures[(key,value)] =featureMap[(key, value)] #adding it to a dict it will be ordered later
                    i+=1

        sortedList = sorted(LineFeatures.items(), key=operator.itemgetter(1))

        #write sorted line to file!(format of liblinear)
        for j in range(i):
            key= sortedList[j][0][0]
            value=sortedList[j][0][1]
            featureIndex=featureMap[(key,value)]
            outputVec.write(str(featureIndex)+':1 ')
        outputVec.write('\n')

    f.close()
    outputVec.close()

    #write available tags in map to reduce MEMM run time(using special chars to split)
    for key,value in availableTags.iteritems():
        outputMap.write('*spc='+str(key)+"&"+'#'.join(list(value))+'\n')
    outputMap.close()


if __name__ == "__main__":
    main()
