'''
Aviv Shisman 206558157  Itay Hassid 209127596
'''



#imports:
from collections import defaultdict
import random
import sys


'''
Main
'''
def main():

    #checking if we got file name
    if len(sys.argv)<=1:
        print "Error, Enter input file"
        return

    #creating the generator
    pcfg = PCFG.from_file(sys.argv[1])

    #in case only input file
    if len(sys.argv)==2:
        print pcfg.random_sent(0)

    #only 2 args can only be FileName -t
    elif len(sys.argv)==3 and sys.argv[2] == '-t':
        print pcfg.random_sent(1)

    #only 3 args can only be FileName -n num
    elif len(sys.argv)==4 and sys.argv[2]=='-n':
        numOfSen = int(sys.argv[3])
        for i in range(numOfSen):
            print pcfg.random_sent(0)
    #both -n num and -t
    elif len(sys.argv)==5 and (sys.argv[2] == '-t' or sys.argv[4] == '-t' ) :
        numOfSen=1
        if sys.argv[2]=='-n':
            numOfSen = int(sys.argv[3])
        elif sys.argv[3] == '-n':
            numOfSen = int(sys.argv[4])

        #print tree structure of all sentences
        for i in range(numOfSen):
            print pcfg.random_sent(1)

    else:
        print 'Wrong Format!'
        print 'The Format is: python programName Filename'
        print 'You can add -n Num(2 args more) to print Num sentences'
        print 'You can add -t (1 argument more) for tree structure'

    return


'''
Their class, generate sentences from grammer
'''
class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    # add rules to grammar
    def add_rule(self, lhs, rhs, weight):
        #check if the (lhs)Src is a single str(like root or s or np)
        assert(isinstance(lhs, str))

        #check if the rhs is a list of derives
        assert(isinstance(rhs, list))

        #add them
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight


    #reading from grammar file and adding rules!
    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            # lines are in format Number/t Src/t Derived (e.g 1 S np vp)
            for line in fh:
                #ignoring lines with #
                line = line.split("#")[0].strip()
                if not line: continue

                w,l,r = line.split(None, 2) # l=Src to develop
                r = r.split()               #r = Derive rules
                w = float(w)                #w=Number
                grammar.add_rule(l,r,w)
        return grammar


    def is_terminal(self, symbol): return symbol not in self._rules


    #flag is 1 if we want tree structure and 0 if we don't
    def gen(self, symbol,flag):
        if self.is_terminal(symbol): return symbol
        else:
            expansion = self.random_expansion(symbol)
            OrignialGen= " ".join(self.gen(s,flag) for s in expansion)
            if flag==1:
                retVal = '(' + symbol + ' ' + OrignialGen + ')'
                return retVal
            return OrignialGen

    def random_sent(self,flag):
        return self.gen("ROOT",flag)

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r



if __name__ == '__main__':
    main()
