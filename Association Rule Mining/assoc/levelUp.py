#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
------------------------------------------------------------------------------
levelUp
    command-line arguments:
        level:     space-sep file of all frequent itemsets of given length k
        trans:     the transaction itemsets
        threshold: the support count requested
        optional - count: space-sep file of all frequent itemsets of given length 1 with its count

------------------------------------------------------------------------------
The input files for level and trans should
* ascii or utf-8 ("txt" file),
* be one itemset per line,
* have items space separated,
* each item is a positive "integer", and
* the items per line should be ordered (e.g., 1 3 5 7 11 ...)

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
# ItemsetDTree(k):
#   * stores itemsets of length k into a hash / dictionary tree
#   * can handle support-counting by feeding in transaction sets
#       * the leaves of the tree are int's; each branch encodes an itemset

class ItemsetDTree:
    iDTree = {}
    iLen   = None

    #-------------------------------------------------------------------------
    # add:
    #     add an itemset to the dictionary-tree

    def add(self, iset, dtree=None):
        if dtree is None: # this is the root call
            dtree = self.iDTree
            if len(iset) != self.iLen:
                print('Trying to add itemset of length %d ' % len(iset)
                      + 'to Tree with item length %d!' % self.iLen)
                exit(-1)
        if len(iset) == 1:
            if iset[0] not in dtree: # first time seen
                dtree[iset[0]] = 0
        else:
            if iset[0] in dtree: # add rest to existing subtree
                self.add(iset[1:],
                         dtree=dtree[iset[0]])
            else:                # build new subtree
                dtree[iset[0]] = self.add(iset[1:],
                                          dtree={})
        return dtree

    #-------------------------------------------------------------------------
    # writeSupported:
    #     print out the itemsets encoded in a dictionary-tree
    #         reportSupport
    #             True:  first int per line ("itemset") is the support count
    #             False: support count not written

    def writeSupported(self,
                       threshold=0,
                       branch='',
                       reportSupport=False,
                       dtree=None):
        if dtree is None: # this is the root call
            dtree = self.iDTree
        for item in sorted(dtree.keys()): # so they come out in sorted order
            if isinstance(dtree[item], int): # at leaf, so write
                if threshold <= dtree[item]:
                    if reportSupport:
                        print(("%d %s %d"
                                % (dtree[item], branch, item)).strip())
                    else:
                        print(("%s %d" % (branch, item)).strip())
            else:                            # recurse down
                self.writeSupported(threshold=threshold,
                                    branch=(branch + ' ' + str(item)),
                                    reportSupport=reportSupport,
                                    dtree=dtree[item])

    #-------------------------------------------------------------------------
    # supportIncr:
    #     increments the support count of each set in the dictionary tree
    #     that is a subset of the transaction set

    def supportIncr(self, tset, dtree=None):
        if dtree is None: # this is the root call
            dtree = self.iDTree
        if len(tset) == 0:
            return;
        if tset[0] in dtree:
            if isinstance(dtree[tset[0]], int):
                dtree[tset[0]] += 1;
            else:
                self.supportIncr(tset[1:],
                                 dtree=dtree[tset[0]])
        self.supportIncr(tset[1:],
                         dtree=dtree)

    #-------------------------------------------------------------------------
    # INIT

    def __init__(self, length):
        if length <= 0:
            print('Itemset length for tree must be positive!')
            exit(-1)
        self.iLen = length

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

#=============================================================================
# MAIN

if __name__ == '__main__':
    k       = 0 # length of itemsets in input level file
    preCNT  = 0 # running tally of pre-candidates produced
    candCNT = 0 # running tally of candidates (after apriori)

    # read first line of level file to measure itemset length
    with open(sys.argv[1], 'r', encoding='utf-8') as inLev:
        for line in inLev:
            line = istrClean(line)
            itemset = string2iset(line.strip('\n'))
            k = len(itemset)
            break
        else:
            print('Empty level file!');
            exit();
            
            
    
    #generate support count dictionary for each item in each item set 
    itemcount = {}
    if len(sys.argv) > 4:
        with open(sys.argv[4], 'r', encoding='utf-8') as inLev:
            for line in inLev:
                line = istrClean(line)
                itemset = string2iset(line.strip('\n'))
                (count, key) = itemset
                itemcount[key] = count
                
        

  
    # read in level file with the frequent itemsets of size k
    #   * store a signature (a string) of the itemset's "prefix", all save
    #     the last item, in a hash / dictionary, to enumerate through
    #     later to do the pre-candidate generation via joining
    #   * store a signature (a string) of the itemset for easy
    #     existence checking during apriori checking
    prefixDict  = {}
    itemsetDict = {}
    with open(sys.argv[1], 'r', encoding='utf-8') as inLev:
        for line in inLev:
            line = istrClean(line)
            itemset = string2iset(line.strip('\n'))
            #sort the item in itemset based on frequencey
            if len(sys.argv) > 4:
                itemset.sort(key=itemcount.get)
            #checking if each itemset has the correct length
            if len(itemset) != k:
                print('Itemset not of length %d read!' % k)
                exit(-1)
            # add the itemset into the prefix signature dictionary
            prefix = iset2string(itemset[:-1])
            if prefix in prefixDict:     # entry already there
                prefixDict[prefix].append(itemset[-1])
            else:                        # create new entry
                prefixDict[prefix] = [itemset[-1]]
            # add the itemset into the itemset signature dictionary
            signature = iset2string(itemset)
            if signature in itemsetDict: # entry seen before
                itemsetDict[signature] += 1
            else:                        # create new entry
                itemsetDict[signature]  = 1

     # if incoming level of itemsets only has one thing, no new candidates!
    if len(itemsetDict) < 2:
        exit()
    
    # put the final-item list per prefix in sorted order
    for prefix in prefixDict:
        if len(sys.argv) > 4:
            prefixDict[prefix] = sorted(prefixDict[prefix], key=itemcount.get)
        else:
            prefixDict[prefix] = sorted(prefixDict[prefix])


    # join on prefixes to create pre-candidates
    # do apriori checks to filter down to candidates
    #   * store the found candidates into a dictionary tree;
    #     their support counts then can be computed efficiently
    #     by iterating over the transactions
    candidates = ItemsetDTree(k+1)
    prefixes   = sorted(prefixDict.keys())
    for prefix in prefixes:
        # join the itemsets with a common prefix
        for i in range(len(prefixDict[prefix]) - 1):
            for j in range(i + 1, len(prefixDict[prefix])):
                itemset = string2iset(prefix)
                itemset.append(prefixDict[prefix][i])
                itemset.append(prefixDict[prefix][j])
                preCNT += 1

                # apriori check the joined pre-candidate!
                apriori = True
                for g in range(len(itemset) - 2):
                    subset = itemset[:g] + itemset[g+1:]
                    if iset2string(subset) not in itemsetDict:
                        apriori = False
                        break
                if apriori:
                    # #sort the item in itemset based on frequencey
                    if len(sys.argv) > 4:
                        itemset = sorted(itemset)
                    candidates.add(itemset)
                    candCNT += 1

    # read in the transaction itemsets, calculate the support counts
    # for the candidates
    with open(sys.argv[2], 'r', encoding='utf-8') as inTrans:
        for line in inTrans:
            line = istrClean(line)
            itemset = string2iset(line.strip('\n'))
            # #sort the item in itemset based on frequencey
            if len(sys.argv) > 4:
                itemset = sorted(itemset)
            candidates.supportIncr(itemset)
            
    endTime = time.time()
    # print out the supported items
    candidates.writeSupported(threshold=int(sys.argv[3]),
                              reportSupport=True)
    
    print('')
    print('#pre-candidates: %d'   % preCNT)
    print('#candidates:     %d'   % candCNT)
    print('Lapsed time:     %.3f' % (endTime - startTime))

