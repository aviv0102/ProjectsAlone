'''
Aviv Shisman 206558157  Itay Hassid 209127596
'''

#imports:
import spacy
import sys
nlp = spacy.load('en')


'''
Our program find the 'Live_in' relations in a corpus
'''
def main():

    print('Hello! Welcome to our relation extractor')
    print('please wait a few seconds...\n')

    if len(sys.argv)!=3:
        print('Error!')
        print('Please insert the following arguments:')
        print('1 - the model we created file (we use it to filter) its called : model.file please enter it as arg1')
        print('2 - the test corpus -> we will exctract the relations from it(Dev)')
        return

    # a ML like approach(not really,explained in writeUp), will be commented in the submit
    # creating the model code:
    #filter_dep1,filter_pos1 = train(sys.argv[1],sys.argv[2]) ---> gets train.corpus and annotations
    #filter_dep2,filter_pos2 = train(sys.argv[3],sys.argv[4]) ---> gets dev.corpus and annotations
    #dep,pos = writeResults(filter_dep1,filter_pos1,filter_dep2,filter_pos2)

    dep,pos=readModel(sys.argv[1])
    relations = find_relations(sys.argv[2],dep,pos)

    print('answers are ready! (result.txt file)\n')

    #f1(relations,sys.argv[3]) --> we previously calculated f1 here


'''
Find relations in test.file
'''
def find_relations(testName,filter_dep,filter_pos):
    relations = []
    sentences = {}  # {index: sentence}
    f = open(testName, 'r')
    for line in f.readlines():

        index, sentence = line.rstrip('\n').split('\t')
        sentences[index] = sentence
        sentence= nlp(sentence)
        entities = list(sentence.ents)

        if len(entities) < 2:
            continue


        #for every couple of different ners in the sentece
        relations_per_sentence=[]
        for ent in entities:
            for other in entities:
                if other != ent:
                    relation = generalize_rules(index, ent, other, sentence)
                    if relation != None:
                        relations_per_sentence.append(relation)

        # after we got all the relations in a sentence we will now filter
        relations_per_sentence = filtering_rules(index,sentence,relations_per_sentence,entities,filter_dep,filter_pos)

        # there might be times we will filter a hole sentence
        if relations_per_sentence !=None:
            relations.extend(relations_per_sentence)
    f.close()

    # write results
    with open('result.txt', 'w') as f:
        for ex in relations:
            f.write('\t'.join(ex) + '\t( ' + sentences[ex[0]] + ')\n')
    return relations


'''
Rules that generalize/generate the sentences and raise the recall (decrease precision)
'''
def generalize_rules(index, ent, other, sentence):

    relation = mainRules(index, ent, other, sentence)

    if relation == None:
        relation = secondRules(index, ent, other, sentence)

    return relation


'''
Main set of rules
'''
def mainRules(index, ent, other, sentence):
    first=''
    second=''
    if (ent.label_ == 'PERSON') and \
            (other.label_ == 'GPE'):  ## or (other.label_ == 'LOC')):
        try:
            if str(sentence[ent.end]) == '.':
                i = 1
            else:
                i = 0
            first = str(sentence[ent.start: ent.end + i])
            if first[-2] == ' ':
                first = first[:-2]

            if str(sentence[other.end]) == '.':
                j = 1
            else:
                j = 0
            second = str(sentence[other.start: other.end + j])
            if second[-2] == ' ':
                second = second[:-2]

        except:
            first = str(sentence[ent.start: ent.end])
            second = str(sentence[other.start: other.end])
        # check title of person
        if ent.start > 0:
            prev_w = sentence[ent.start - 1].text
            # if prev_w.istitle() and prev_w.endswith('.'):
            if prev_w in ['Mrs.', 'Dr.', 'Ms.']:
                first = sentence[ent.start - 1: ent.end + i].text
        return (index, first, 'Live_In', second)
    else:
        return None

'''
Second set of rules
'''
def secondRules(index, ent, other, sentence):



    first = ent.text
    # in case we changed the original, do not change this

    if ent.start > 0 :
        prev_w = sentence[ent.start - 1].text
        if prev_w in ['Mrs.', 'Dr.', 'Ms.']:
            first = sentence[ent.start - 1: ent.end].text

    # Check if there is preposition and a location after it
    # (e.g 'aviv .... of israel)
    try:
        radius = 10
        preps=['IN','OF']

        if ent.label_=='PERSON' :
            for i,word in enumerate(sentence):
                cur = str(word.text).upper()
                if cur in preps and sentence[i+1].is_title\
                        and not sentence[i+2].is_title and (i-ent.start)<radius and i-ent.start>0:

                    return (index, first, 'Live_In',sentence[i+1].text)
    except:
        pass

    # Check options where the other is ORG/PERSON instead of GEO
    try:
        radius = 2
        if (ent.label_ == 'PERSON' ) and \
                (other.label_ == 'ORG' or other.label_ == 'PERSON' ):
            if other.root.is_title and other.root.pos_ == 'PROPN' and \
                    abs(ent.start - other.start) < radius:
                return (index, first, 'Live_In', other.text)

    except:
        pass

    # for a few rare cases like soviet
    try:
        radius = 3
        if (ent.label_ == 'PERSON') and  (other.label_ == 'NORP'):
            if other.root.is_title and other.root.pos_ == 'PROPN' and \
                    abs(ent.start - other.start) < radius:
                return (index, first, 'Live_In', other.text)

    except:
        pass

    # check if name is ORG and other is GPE
    try:
        radius = 4
        if (ent.label_ == 'ORG' ) and \
                (other.label_ == 'GPE'):
            if abs(ent.start - other.start) < radius:
                return (index, first, 'Live_In', other.text)

    except:
        pass




    return None


'''
filtering some of the relations (increase precision decease recall)
'''
def filtering_rules(index, sentence, relations,entities,filter_dep,filter_pos):
    
    # first filter remove copies:
    new_relations = list(set(relations))

    # second filter relation where the the 'person' entity is not a person .
    for rel in new_relations.copy():
        for ent in entities:
            if not ent.text in rel[1]:
                continue
            before = sentence[ent.start-1]
            if before.text == '-' or before.text=='at':
                try:
                    new_relations.remove(rel)
                except:
                    pass

    # third filter -> find suspected sentences and remove some
    flag = False
    count = 0
    treshold = 2
    for ent in entities:
        if ent.label_ == 'DATE' or ent.label_ == 'TIME' or ent.label_ == 'LOC' or ent.label_ == 'ORDINAL' or\
        ent.label_=='QUANTITY':
            flag = True
            count += 1

    # if sentence is focused on something not related to live_in
    if count > treshold:
            return None

    # 4th filter , using the train:
    for rel in new_relations.copy():
        first_dep_label = ''
        first_pos_label = ''
        second_dep_label = ''
        second_pos_label = ''
        for ent in entities:
            if ent.text in rel[1]:
                first_dep_label = ent.root.dep_
                first_pos_label = ent.root.pos_
            if ent.text in rel[3]:
                second_dep_label = ent.root.dep_
                second_pos_label = ent.root.pos_

        relation_dep = (first_dep_label, second_dep_label)
        relation_pos = (first_pos_label, second_pos_label)

        if not relation_dep in filter_dep.keys() or not relation_pos in filter_pos.keys():
            new_relations.remove(rel)

    # 5th filter name,GPE with great distance if the sentence is suspect
    rad = 10 # ---> best f1 score
    for rel in new_relations.copy():
        loc_a = -1
        loc_b = -1
        for ent in entities:
            if ent.text in rel[1]:
                loc_a=ent.start
            if ent.text in rel[3]:
                loc_b =ent.start

            if not (loc_a==-1 or loc_b==-1):
                if abs(loc_a-loc_b)>rad:
                    try:
                        new_relations.remove(rel)
                        break
                    except:
                        pass

    # 6th rule only for suspects:
    if flag==True:
        relationEnts = {}
        for i, rel in enumerate(new_relations):
            first = second = None
            for ent in entities:
                if ent.text in rel[1]:
                    first = ent
                if ent.text in rel[3]:
                    second = ent
            if first is not None and second is not None:
                if second not in relationEnts:
                    relationEnts[second] = []
                relationEnts[second].append((rel[0], first, 'Live_In', second, rel))

        for rel in new_relations.copy():
            if rel[1] == rel[3]:
                new_relations.remove(rel)

            try:
                for ent in entities:
                    if ent.text in rel[1]:
                        gpes = list(ent.subtree)
                        for i in gpes.copy():
                            gpes.extend(i.subtree)
                        flag = False
                        for place in [gpe.text for gpe in gpes]:
                            if rel[3] in place:
                                flag = True
                        if not flag:
                            for arr in relationEnts.values():
                                for element in arr:
                                    if element[4] == rel:
                                        if abs(element[1].start - element[3].start) < 8:
                                            flag = True
                        if not flag:
                            new_relations.remove(rel)
            except:
                print(index)

    return new_relations


'''
calculate f1,recall,precision using the annotations file(testPred) and relations(our pred)
notice that we don't use it anymore because we moved it to eval.py
also notice here we did error analysis (files : not found, need to filter)
'''
def f1(relations,testPredName):
    dev_annotations = []
    f = open(testPredName, 'r')
    g = open('not found.txt', 'w')
    g2 = open('need to filter', 'w')

    # getting the relations
    counter=0
    for line in f.readlines():
        splited = line.rstrip('\n').split('\t')
        if splited[2] == 'Live_In':
            counter+=1
            annot = tuple(splited[:4])
            dev_annotations.append(annot)
            if annot not in relations:
                 g.write(line+'\n')
    f.close()
    g.close()

    # calculate true and false positive
    truePositive = 0
    falsePostive=0
    for example in relations:
        if example in dev_annotations:
            truePositive += 1
        else:
            falsePostive+=1
            g2.write(str(example)+'\n')     #false pos => need to filter

    # calculate false negative (no need to filter...)
    falseNeg=0
    for e in dev_annotations:
        if not e in relations:
            falseNeg+=1


    recall = 1.0*truePositive/(truePositive+falseNeg)
    precision = 1.0*truePositive/(truePositive+falsePostive)
    f1_score = 2*((precision*recall)/(precision+recall))
    print('recall=', recall, ', precision= ',
          precision, ', f1= ', f1_score)


'''
reading the "model" from file
'''
def readModel(modelName):

    dep = {}
    pos = {}
    modelInput = open(modelName,'r')
    flag= 0     #means we reading the
    for line in modelInput.readlines():
        if line in '***\n':
            flag =1
            continue
        token,value=line.rstrip('\n').split(' ')
        temp = token.split(',')
        rel = (temp[0], temp[1])
        if flag ==0:
            dep[rel] = int(value)
        if flag ==1:
            pos[rel] = int(value)



    return dep,pos

'''
creating a model that help us to filter (not really ML) , was used one time and now we only read the model
'''
def train(corpusName,annotationsName):

    # get all the sentences in train that have Live_in in them
    passed_dict = {}
    annotations = open(annotationsName,'r')
    for line in annotations.readlines():
        line = line.split()
        flag = False
        first = ''
        second = ''
        for i,word in enumerate(line):
            if word == '(':
                break
            if word!='Live_In' and flag==False and i!=0:
                first += word + ' '
            if word!='Live_In' and flag==True and i!=0:
                second +=word + ' '
            if word == 'Live_In':
                flag=True
        # if its live_in realtion add it and later we will count it
        if flag==True:
            if not line[0] in passed_dict.keys():
                passed_dict[line[0]] =[]
                passed_dict[line[0]].append ((first, second))
            else:
                passed_dict[line[0]].append ((first, second))

    annotations.close()

    corpus = open(corpusName,'r')

    # use later to filter by dep
    filter_dep_info = {}

    # use later to filter by pos
    filter_pos_info = {}

    # we now will iterate over each relation and get its dependency tag and put it in to a dictionary
    for line in corpus.readlines():
        index, sentence = line.rstrip('\n').split('\t')
        line = line.split()
        if line[0] in passed_dict.keys():
            sentence = nlp(sentence)
            entities = list(sentence.ents)
            for tuple in passed_dict[line[0]]:                      # some lines have 2 or more relations
                first,second = tuple
                for ent in entities:
                    if ent.text in first:
                        first_dep_label = ent.root.dep_
                        first_pos_label = ent.root.pos_
                    if ent.text in second:
                        second_dep_label = ent.root.dep_
                        second_pos_label = ent.root.pos_

                try:
                  add_dict(filter_dep_info,first_dep_label,second_dep_label)
                  add_dict(filter_pos_info,first_pos_label,second_pos_label)
                except:
                    pass

    corpus.close()
    return filter_dep_info,filter_pos_info

'''
help function
'''
def add_dict(filter_info,first_label,second_label):

    if (first_label, second_label) in filter_info.keys():
        filter_info[(first_label, second_label)] += 1
    else:
        filter_info[(first_label, second_label)] = 1

'''
Write model to file
'''
def writeResults(dep1,pos1,dep2,pos2):

    dep = {}
    for rel in dep1:
        dep[rel] = dep1[rel]
    for rel in dep2:
        if rel in dep.keys():
            dep[rel] += dep2[rel]
        else:
            dep[rel] = dep2[rel]

    pos = {}
    for rel in pos1:
        pos[rel] = pos1[rel]
    for rel in pos2:
        if rel in pos.keys():
            pos[rel] += pos2[rel]
        else:
            pos[rel] = pos2[rel]

    modelOut = open ('model.file','w')

    for rel in dep:
        modelOut.write(rel[0]+ ','+rel[1] +' '+str(dep[rel]))
        modelOut.write('\n')
    modelOut.write('***\n')

    for rel in pos:
        modelOut.write(rel[0] + ',' + rel[1] + ' ' + str(pos[rel]))
        modelOut.write('\n')
    modelOut.write('***')

    modelOut.close()




if __name__ == '__main__':
    main()
