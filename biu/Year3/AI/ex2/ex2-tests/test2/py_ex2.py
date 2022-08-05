'''
aviv shisman
206558157
'''

from queue import PriorityQueue
import sys
import math

'''
Main , classifying with 3 different methods
'''
def main():
    if len(sys.argv)<3:
        print('Error, please enter the following: train and test file')
        print( '1 - the train file for the models')
        print( '2 - the test file which you want to get the predictions on')
        return

    # load info
    train,test=loadInfo(sys.argv[1],sys.argv[2])

    print('Results: (please read ReadME file)\n')

    # activate models:

    knn_answer = KNN(train,test)
    nb_answer = naiveBayes(train, test)
    dt_answer = decisionTree(test,sys.argv[1],sys.argv[2])

    writeResults(knn_answer,nb_answer,dt_answer)

    return


# <------------------------------------------------ functions we used for all models ------------------------------>

'''
Loading the train and test
'''
def loadInfo(trainName,testName):
    trainFile = open(trainName,'r')
    testFile = open(testName,'r')

    train=[]
    for i,line in enumerate(trainFile.readlines()):
        if i==0:
            continue
        l=line.strip().split()
        train.append(l)
    test=[]
    for i,line in enumerate(testFile.readlines()):
        if i==0:
            continue
        l=line.strip().split()
        test.append(l)

    return train,test

'''
get accuracy of each model
'''
def pred(test,answer,algName):

    correct=0
    size=0
    for i,ex in enumerate(test):
        if answer[i]==getXClass(test[i]):
            correct+=1
        size+=1

    print('prediction of '+algName+' was: '+str(answer))

    precision = math.ceil(100* (correct/size))/100

    print('precision is :'+str(precision) +'\n')


    return precision

'''
write results in the format requested
'''
def writeResults(knn_answer,nb_answer,dt_answer):

    f = open ("output.txt",'w')
    f.write('‫‪Num'+'\t'+'DT‬'+'\t'+'KNN'+'\t'+'naiveBase‬\n')
    for i in range(len(knn_answer[0])):
        f.write(str(i+1)+'\t'+dt_answer[0][i]+'\t'+knn_answer[0][i]+'\t'+nb_answer[0][i]+'\n')
    f.write('\t' + str(dt_answer[1]) + '\t' + str(knn_answer[1]) + '\t' + str(nb_answer[1])+'\n')

    return

'''
get the class of example x
'''
def getXClass(x):
    ans=x[len(x)-1]
    return ans

'''
add +1 to dict in entry key
if entry don't exist reset its value to 1
'''
def addCountToDict(dict,key):
    if not key in dict.keys():
        dict[key] = 1
    else:
        dict[key] += 1
    return




# <---------------------------------------- Start of KNN --------------------------------------------------------->

'''
First method, using knn algorithm (notice this algorithm don't have train stage like most ML algorithems, 
its training is to load the examples to memory.)
'''
def KNN(train,test):

    k=5
    answer=[]
    for i,example in enumerate(test):

        #remove x class for not counting it as a feature
        x=example[:-1]

        # get the k closest neighbors
        q = PriorityQueue()
        for j,y in enumerate(train):
            dis=calcDistance(x,y)
            cls= getXClass(y)
            q.put(Neighbor(cls,dis,j))

        # get count the neighbors "votes"
        dict={}
        for i in range(k):
            neighbor=q.get()
            cls=neighbor.cls
            addCountToDict(dict,cls)

        # get the max vote
        max=-1
        maxClass=''
        for cls in dict.keys():
            if dict[cls]>max:
                max=dict[cls]
                maxClass=cls
        answer.append(maxClass)

    prec = pred(test,answer,'KNN')



    return answer,prec

'''
calculate distance of vectors for knn functiion
'''
def calcDistance(x,y):
    dis=0
    for i in range(len(x)):
        if x[i]!=y[i]:
            dis+=1

    return dis

'''
class for sorting the neighbors by distance and then by arrival like you stated
'''
class Neighbor:

    def __init__(self,cls,dis,arrival):
            self.cls=cls
            self.distance=dis
            self.arrival=arrival

    def __lt__(self, other):
        #try order by distance else by arrival time
        if self.distance==other.distance:
            return self.arrival<other.arrival
        else:
            return  self.distance<other.distance



# < ------------------------------------- Start of naive Bayes --------------------------------------------------->
'''
Second method, naiveBase
'''
def naiveBayes(train, test):

    #train:
    p_c,p_x_c=trainModel(train)

    #prediction:
    answers=[]
    for i,example in enumerate(test):

        #remove tagging to not interfere with our prediction
        x=example[:-1]


        # get the argmax of p(c) * Py over i :(p(x|c))
        if i==11:
            print('s')
        max=-1
        argMax=''
        for cls in p_c:
            mult=1
            for (y,c) in p_x_c:
                if c!=cls or y not in x:
                    continue
                j=0
                for k in example:   # in cases we have the same attribute occuring twice or more = [crew,crew,male]
                    if k==y:
                        mult*= p_x_c[(y,c)]
            value= p_c [cls]*mult

            if value>max:
                max=value
                argMax=cls

        answers.append(argMax)


    prec = pred(test,answers,'naiveBayes')

    return answers,prec

'''
train naiveBase model
'''
def trainModel(train):

    #params
    p_c={}              # probability for class c  -- dictionary (each class has prob)
    p_x_c={}            # prob for (word,class)    -- dictionary (each word,class has prob)
    count_class={}      # count number of class    -- dictionary (each class has count)
    count_word={}       # count number of word     -- dictionary (each word  has count)
    count_class_word={} # count number of class,word
    col_count={}        # count number of options per feature
    helpDict={}         # for col_count
    vocab=set()         # all words in train set

    # count for p_c prob: (like in lecture)
    for i,x in enumerate(train):
        cls=getXClass(x)
        addCountToDict(count_class,cls)
    # calc p_c prob
    for cls in count_class:
        p_c[cls]=count_class[cls]/len(train)

    # count for p_x_c prob:
    for i,example in enumerate(train):
        x=example[:-1]
        cls=getXClass(example)
        for i,word in enumerate(x):
            addCountToDict(count_word,word)
            addCountToDict(count_class_word,(cls,word))
            vocab.add((word,i))
            if not (word,i) in helpDict:
                helpDict[(word,i)]= 1

    # calc k for prob
    for (word,i) in helpDict:
        addCountToDict(col_count,i)

    # calc p_x_c prob :
    for (word,i) in vocab:
        for cls in p_c:
            try:
                top = count_class_word[(cls,word)]+1         # count(class,word)+1
            except:
                top= 1
            bottom = count_class[cls] + col_count[i]     # count(class) + col_count-->k for smoothing
            p_x_c[(word,cls)]= top/bottom


    return p_c,p_x_c





# <--------------------------------------Start of Decision trees -------------------------------------------------->

'''
Third model, decision tree...
'''
def decisionTree(test,trainName,testName):

    #params:
    X,Y,head = DT_loadinfo(trainName)
    possible_atts = get_possible_atts(X)
    params= DTParams(X,Y,head,possible_atts)
    defult = mode(list(zip(X, Y)))
    data = list(zip(X, Y))


    #build tree
    tree = ID3(data, head[:],defult , params)
    params.addTree(tree)

    #predicte
    answers=DT_output(params, testName)

    #accuracy
    prec=pred(test,answers,'DT')

    #write to file
    tree_to_file(params)

    return answers,prec


'''
ID3 algorithm , also known as DTL , i used the code from lecture
'''
def ID3(data, atts, defult, params):

    #parameters
    tree = {}
    heads = params.heads
    possible_atts = params.possible_atts

    # are all the examples the same classification?
    Is_all_example_same_classification ,possible_cls= are_all_same(data)

    # if data is empty return defult
    if data == []:
        return defult
    # if all the examples have the same classification
    if Is_all_example_same_classification:
        return possible_cls
    # if atts is empty return mode(examples) like in psudo code
    if (atts is None or atts == []):
        return mode(data)

    # get the att with highest gain
    best_att_idx = choose_att_idx_by_gain(data, atts, params)
    best_att = possible_atts [best_att_idx]

    # create a new tree with the root best
    tree[heads[best_att_idx]] = {}

    for vi in best_att:
        examples_i = get_attv_matches(data, best_att_idx, vi)
        atts.remove(heads[best_att_idx])
        defult2 = mode(data)
        sub_tree = ID3(examples_i, atts, defult2, params)
        atts.append(heads[best_att_idx])

        tree[heads[best_att_idx]].update({vi: sub_tree})

    return tree



# <---------------------------------------help functions/class------------------------------>
'''
load info in the format we need for DT
'''
def DT_loadinfo(file_name):
    X = []
    Y = []
    catagorize = []

    f = open(file_name,'r')

    for i,line in enumerate(f.readlines()):
        l=line.strip().split()

        if i==0:
            catagorize=l[:-1]
            continue
        cls= getXClass(l)
        X.append(l[:-1])
        Y.append(cls)

    return X,Y,catagorize


'''
get the highest vote
'''
def mode(examples):

    count_dict = {}
    for ex in examples:
        addCountToDict(count_dict,getXClass(ex))

    max=-1
    argMax=''
    for cls in count_dict:
        if count_dict[cls]>max:
            argMax=cls
            max = count_dict[cls]

    return  argMax


'''
check if all the examples have the same tag, if it does return (true, classification)
'''
def are_all_same(ex):

    possible_classes= list(set([y for x, y in ex]))     #the data changes between the runs
    if (len(possible_classes) == 1):
        return True,possible_classes[0]
    return False,None


'''
get the possible attributes for each category
'''
def get_possible_atts(Xdata):

    #parameters:
    attList = []
    length = len(Xdata[0])

    # creating list for possible atts
    for i in range(length):
        attList.append([])

    # copying possible att to list
    for att in Xdata:
        for i in range(length):
            attList[i].append(att[i])
    # we don't want copies
    for i, l in enumerate(attList):
        attList[i] = list(set(l))

    return attList


'''
get count for each class (e.g 'yes':400 'no':600)
'''
def get_class_count(data):
    count_class = {}
    for atts,cls in data:
        addCountToDict(count_class,cls)
    return list(count_class.values())


'''
Info class
'''
class DTParams:
    def __init__(self,x,y,heads,possible_atts):
        self.X=x
        self.Y=y
        self.heads = heads
        self.possible_atts = possible_atts

    def addTree(self,tree):
        self.Tree=tree


'''
check how meny examples in curr data have the current attribute val in their index(th) place -> used for entropy_T_X
'''
def count_attV_matches(data, idx, val):
    counter = 0
    for atts, tag in data:
        if atts[idx] == val:
            counter += 1
    return counter


'''
get all the matches and not just count them 
'''
def get_attv_matches(data, idx, val):
    res = []
    for atts, tag in data:
        if atts[idx] == val:
            res.append((atts, tag))
    return res


# <------------------------------------calculation functions----------------------------->
'''
choose the best att with the highest gain value
'''
def choose_att_idx_by_gain(data, atts, params):

    main_atts = params.heads
    att_idx = -1
    maxVal = -111

    for i,att in enumerate(main_atts):
        if att not in atts:
            continue
        else:
            val = gain(data, i)
            if val>maxVal:
                maxVal = val
                att_idx = i
    return att_idx


'''
calc gain like we learned in presentation
'''
def gain(data, att_idx):


    # calc freq_ent
    data_without_class = [x for x, y in data]
    possible_atts = get_possible_atts(data_without_class)[att_idx]
    ent_t_x =entropy_T_X(data, possible_atts, att_idx)

    # calc ent
    en = entropy(get_class_count(data))


    # gain = ent(x) - ent (t,x)
    return en - ent_t_x

'''
calculate entropy(T)  --> entropy(golf)
'''
def entropy(count_class_list):

    # parameters:
    res = 0
    sum_count_list = sum(count_class_list)

    # calculate by lecture 8 code:
    for class_count in count_class_list:
        first = (class_count / sum_count_list)
        second =  math.log2(class_count / sum_count_list)
        res -=  first * second
    return res


'''
calc entropy(T,X) --> entropy(golf,Windy)
'''
def entropy_T_X(data, possible_atts, idx):
    res = 0
    for attv in possible_atts:
        first = count_attV_matches(data, idx, attv) / len(data)
        second = entropy(get_class_count(get_attv_matches(data, idx, attv)))
        res += first * second
    return res



# <-------------------------------------- getting DT Results: --------------------------->

'''
print tree to a file
'''
def print_tree(f, tree, V, needToWrite="", k=0):

    if (V == 'v'):
        key = sorted(list(tree.keys()))[k]
        if (type(tree[key]) == str):
            print(key + ":" + tree[key], file=f)
        else:
            print(key, file=f)
            print_tree(f, tree[key], 'a', needToWrite + '\t', 0)
    else:
        for key, val in tree.items():
            for i in range(len(val)):
                if (k != -1):
                    print(needToWrite + "|" + key + "=", end='', flush=True, file=f)
                else:
                    print(key + "=", end='', flush=True, file=f)
                print_tree(f, val, 'v', needToWrite, i)

'''
predict for example
'''
def DT_prediction(params, example):

    #params:
    tree = params.Tree
    heads = params.heads
    treeC = tree.copy()
    root = list(tree.keys())[0]


    while (type(treeC[root]) != str):
        idx = heads.index(root)
        value_of_att = example[idx]
        if (type(treeC[root][value_of_att]) == str):
            return treeC[root][value_of_att]
        treeC = treeC[root][value_of_att]
        root = list(treeC.keys())[0]
    print(treeC[root])

'''
get all predictions 
'''
def DT_output(params, test_file_name):

    test_x, test_y, _ = DT_loadinfo(test_file_name)
    pred = []
    for xt, yt in zip(test_x, test_y):
        pr = DT_prediction(params, xt)
        pred.append(pr)

    return pred

'''
write tree to file
'''
def tree_to_file(params):
    with open("output_tree.txt", 'w') as file:
         print_tree(file,params.Tree, 'a', "", -1)


# ----------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
