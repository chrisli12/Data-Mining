#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
------------------------------------------------------------------------------
arules.py
    command-line arguments:
        j-frequent item:     the frequent itemsets of length j with their support counts
        k-frequent item:     the frequent itemsets of length k with their support counts
        threshold: a confidence threshold p

------------------------------------------------------------------------------
The input files for level and trans should
* ascii or utf-8 ("txt" file),
* be one itemset per line,
* have items space separated,
* each item is a positive "integer", and
* the items per line should be ordered (e.g., 1 3 5 7 11 ...)
* the first element must be the count of the itemset

------------------------------------------------------------------------------
    
       author: Chun Ho Li
  attribution: "levelUp.py" by parke godfrey licensed under CC / modification from original
     creation: 2021-02-15
last modified: 2021-02-19
     language: python 3
      license: CC, any reuse and modification, with attribution
------------------------------------------------------------------------------
'''
#=============================================================================
import sys
import time

startTime = time.time()

#=============================================================================
# FUNCTIONS

# itemset / iset: an ordered list of int's representing an itemset
#                 we use int's not strings to make this more efficient
def istrClean(istr):
    istr = ' '.join(istr.strip('\n').split())
    for token in istr.split():
        if not token.isnumeric():
            print('Item "%s" is not an integer!' % token)
            exit(-1)
    return istr

def string2iset(istr):
    return [int(token) for token in istr.split()]

def iset2string(iset):
    itok = [str(item) for item in iset]
    return ' '.join(itok)

#powerset: generate the all the subet of leght l of the set s
def powerset(s, j):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        if len([ss for mask, ss in zip(masks, s) if i & mask]) == j:
            yield ([ss for mask, ss in zip(masks, s) if i & mask])
    
#=============================================================================
# MAIN

if __name__ == '__main__':
    j = 0 # length of itemsets in input level file
    k  = 0 # running tally of pre-candidates produced
    confidence = float(sys.argv[3]) # running tally of candidates (after apriori)

    # read first line of j file to measure itemset length
    with open(sys.argv[1], 'r', encoding='utf-8') as inLev:
        for line in inLev:
            line = istrClean(line)
            itemset = string2iset(line.strip('\n'))
            j = len(itemset) - 1
            break
        else:
            print('Empty input file!');
            exit();
   # read first line of k file to measure itemset length
    with open(sys.argv[2], 'r', encoding='utf-8') as inLev:
        for line in inLev:
            line = istrClean(line)
            itemset = string2iset(line.strip('\n'))
            k = len(itemset) - 1
            break
        else:
            print('Empty input file!');
            exit();
            
    if (0<j<k == False):
        print('Incorrect legth of the frequent itemsets files!')
        exit();
    
    if(0 <= confidence <= 1 == False):
        print('Confidence error: confidence should be within 0 to 1!')
        exit();
            
        
    j_itemsets = {} 
    #adding 4-itemsets_j to dictionary, use itemset
    with open(sys.argv[1], 'r', encoding='utf-8') as file_j:
        for line_j in file_j:
           line_j = istrClean(line_j)
           itemwcount_j = string2iset(line_j.strip('\n'))
           count_j = itemwcount_j[0]
           itemset_k = iset2string(itemwcount_j[1:])
           j_itemsets[itemset_k] = count_j
       
    #assocation rules dictionary for each item in each item set 
    arulesDict = {}
    rulescount = 0 
    #adding 6-itemsets_k to ItemDTree      
    with open(sys.argv[2], 'r', encoding='utf-8') as file_k:
        for line_k in file_k:
            line_k = istrClean(line_k)
            itemwcount_k = string2iset(line_k.strip('\n'))
            count_k = itemwcount_k[0]
            itemset_k = itemwcount_k[1:]
            #generate all subset of length j 
            for subset in powerset(itemset_k, j):
                if iset2string(subset) in j_itemsets:
                    #calculate the confindence
                    if count_k/j_itemsets[iset2string(subset)] >= confidence:
                        rule = iset2string(subset) + ' => ' + iset2string([x for x in itemset_k if x not in subset])
                        conf = count_k/j_itemsets[iset2string(subset)]
                        arulesDict[rule] = conf
                        rulescount += 1
                   
                    
    endTime = time.time()
    
    #print out the rules
    for rule, conf in arulesDict.items():
        print('%.3f' % conf, " ", rule)

    print('')
    print('#rules:     %d'   % rulescount())
    print('Lapsed time:     %.3f' % (endTime - startTime))