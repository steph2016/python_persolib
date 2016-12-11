
import numpy as np

class combo:
    def __init__(self,listindices=[],totalvalue=0,previouscombo=None):
        if isinstance(previouscombo,combo):
            self.listindices = previouscombo.listindices + listindices
        else:
            self.listindices = listindices
        self.totalvalue = totalvalue

def npermutations(liste,length):# adapted from http://stackoverflow.com/questions/16453188/counting-permuations-in-python
    import operator
    from collections import Counter
    from functools import reduce
    num = np.math.factorial(length)
    
    # how many 0 in the list ?
    n0 = length - len(liste)
    
    mults = list(Counter(liste).values()) + [n0]
    den = reduce(operator.mul, (np.math.factorial(v) for v in mults), 1)
    return num / den
    
def combo_to_get_a_sum(numbers,total,nlimit=9,single_shot=False,proba=False):
    r"""
    compute all possible combinations of numbers from a given set, to have the sum equal to a given value.
    - possible to choose the depth (ie. the maximum number of numbers in a combination)
    - possible to choose whether a number of the set can be chosen several times or only once, in a combination 
    - the set in input may contain several times the same number and is not necessarily ordered
    if everal times the same number while an element may be chosen only once, then each number of the set (even if they have the same value) can be chosen once
    - possible to associate in input probabilities to the numbers (so there is a set of probabilities in input together with the set of numbers)
    and to compute the probability of each combination, together with the total probability
    
    hypothesis: all numbers of the set are positive
    
    numbers: 1D list or array of numbers (not void & no 0). this is the set
    total: float>0, sum to reach
    nlimit: int>=0, upper nlimit on the number of indices that can be listed
    single_shot: boolean, if False then a given index can be chosen several times
    proba: if 1D list or array of the same dmension than numbers, then probas are interpreted as the probilities of numbers and in output each combination has a proba. Also computation of the total proba
    
    returns a list of all possible combo (ie. len(returned)==number of combo)
    each element of the list is a combo objects with indices corresponding to the SORTED set of numbers
    
    todo: verifying inputs
    - numbers is 1D, not void, without any 0, WITH ONLY POSITIVE NUMBERS !!!
    - nlimit integer>0
    """
    niter = 1
    listsoluces = [] # list of combos that are ok
    listsoluces_cur = [combo()] # list of combos that are under calculation
    numbs = np.sort(numbers)
    # if single_shot, then the probability is quite simple to compute: it's just product(proba) x #permutations
    # but if not single_shot, then probabilities must be corrected by the # of identical permutations
    calcproba = isinstance(proba,np.ndarray)
    if calcproba:
        if len(proba)!=len(numbs):
            print('warning: proba array not understood...')
            calcproba = False
    #calcproba_complex = calcproba and single_shot
    if calcproba:
        indnumbs = np.argsort(numbers)
    #    p = p_cur = []
    #if calcproba_complex:
    #    pcounter = np.zeros(len(numbs))        
    maxindex = len(numbs)-1

    while niter <= nlimit:
        listnew = [] # list of new indices : the first one is the original list (ie.from previous iteration);
            #after there are new lists, so if there is more than 0 newlists
            #the original one must be replaced by new ones
            #else the branch can be cut out
        #if calcproba:
        #    listnewp = []
            
        for i,j in enumerate(listsoluces_cur):
            listnew.append([]) # listnnew could be initialised to have directly len(listsoluces) elements. but what is the syntaxe ?!
            #if calcproba:
            #    listnewp = ([])
            if niter>1:
                maxindex = j.listindices[-1]# just add '-1' for single_shot ?
                if single_shot:
                    maxindex -= 1

            # to exclude too large values
            maxnumber = total - j.totalvalue
            while numbs[maxindex] > maxnumber:
                maxindex -= 1
            ###########################

            for k in range(maxindex+1):
                listnew[-1].append([k,j.totalvalue + numbs[k]])
                #if calcproba:
                    
                    
                #print('debug 1: ',listnew,j.totalvalue,numbs[k])                  
                    
        nremoved=0        
        for i,j in enumerate(listnew):
            temp = listsoluces_cur.pop(i-nremoved)
            nremoved +=1
        
            #print('debug 2: ',i,j,temp.listindices,temp.totalvalue)        
        
            for k,l in enumerate(j):
                if l[1] == total:
   #                 print('debug 5')
                    lll = listsoluces
                else:
                    lll = listsoluces_cur
                lll.append(combo(previouscombo=temp,listindices=[l[0]],totalvalue=l[1]))
    
#        for i,j in enumerate(listsoluces_cur):
#            print('debug 3: ',i,j,j.listindices,j.totalvalue)
#        for i,j in enumerate(listsoluces):
#            print('debug 4: ',i,j,j.listindices,j.totalvalue)
#        print('debug 6: ',len(listsoluces_cur),len(listsoluces))
#        #import pdb; pdb.set_trace()
        
        niter += 1
        
    if calcproba:
        p = np.ones(len(listsoluces))
        for i,j in enumerate(listsoluces):
            for k,l in enumerate(j.listindices):            
                p[i] *= proba[indnumbs[l]]
            # number of permutation in a sequence of nlimit values, where only not null values are referenced here
            p[i] *= npermutations(j.listindices,nlimit)
            # mult by the proba to have 0 every where else
            p[i] *= (1 - np.sum(proba))**(nlimit-len(j.listindices))
        return listsoluces, p
    else:    
        return listsoluces            
    
   