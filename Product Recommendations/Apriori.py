import pandas as pd
import time 
# support
SUPPORT = 100

# Create list of baskets
def make_baskets():
    basket_list = []
    dataFile = open("browsing-data.txt", "r")
    entries = 0
    for line in dataFile:
        # add list of item on the line as a basket element in the list
        basket_list.append(line.split())
        entries += 1
    return basket_list, entries


# Create candidate itemsets (Ck)
def make_candidates(datasets):
    # Store items and their counts in a dictionary
    cand = {}
    # iterate through items in all baskets
    # if the item not in the dict yet, add item as key and init its count with 1
    # else increment the item's count in dict
    for basket in datasets:
        for item in basket:
            # check if item in dictionary
            if item in cand:
                cand[item] += 1
            else:
                cand[item] = 1
    # number of unique values: 12592
    return cand


# Create frequent itemsets (Lk)
def freq_itemsets(Ck):
    for item in list(Ck.keys()):
        if Ck[item] < SUPPORT: # if < than support, remove item
            Ck.pop(item)
    # number of freq items: 647
    return Ck

# Create candidate set C2 from L1
from itertools import combinations
def freq_pairs(freqList, baskets):
    # dictionary of pairs and their counts
    c_dict = {}
    # for each basket, look in the frequent items list to see which of its items are frequent
    # doing this further minimize the frequent pair list
    for bas in baskets:
        freq_items = []
        for item in bas:
            if item in freqList:
                freq_items.append(item)
        # generate all pairs of frequent items in the basket
        c_list = [tuple(sorted(p)) for p in list(combinations(freq_items,2))]
        # if dict is empty, init pair count with 1
        # else add 1 to count
        for pair in c_list:
            if pair in c_dict:
                c_dict[pair] += 1
            else:
                c_dict[pair] = 1
    
    # filter out low support pairs
    for pair, count in list(c_dict.items()):
        if count < SUPPORT:
            c_dict.pop(pair)
    
    # time inefficient
    ''' 
    for pair in c_set:
        count = 0
        for bas in baskets:
            #if pair[0] in bas and pair[1] in bas:
            #if all(item in bas for item in pair):
            if set(pair) <= set(bas):
                count += 1
        if count >= SUPPORT:
            c_dict[pair] = count
    '''       
    return c_dict

def freq_triples(freqList, baskets):
    # dictionary for triplets and their counts
    c_dict = {}
    # for each basket, look in the frequent items list to see which of its items are frequent
    for bas in baskets:
        freq_items = []
        for item in bas:
            if item in freqList:
                freq_items.append(item)
        # generate all triplets of frequent items in the basket
        c_list = [tuple(sorted(t)) for t in list(combinations(freq_items,3))]
        # if dict is empty, initialize triplet count with 1
        # else add 1 to count
        for trip in c_list:
            if trip in c_dict:
                c_dict[trip] += 1
            else:
                c_dict[trip] = 1    
    # filter out low support pairs       
    for trip, count in list(c_dict.items()):
        if count < SUPPORT:
            c_dict.pop(trip)

    return c_dict

def confidence_pairs(freq_dict, freq_items):
    rules_dict = {}
    for k, v in freq_dict.items():
        # x->y
        rule1 = k[0] + "=>" + k[1]
        score1 = v/freq_items[k[0]]
        rules_dict[rule1] = score1
        # y->x
        rule2 = k[1] + "=>" + k[0]
        score2 = v/freq_items[k[1]]
        rules_dict[rule2] = score2
    top5Rules = sorted(rules_dict.items(), key = lambda item:item[1], reverse=True)
    return top5Rules[:5]

def confidence_triples(freq_dict, freq_pairs):
    rules_dict = {}
    for k, v in freq_dict.items():
        # x, y -> z
        rule1 = k[0] + " " + k[1] + " " + k[2]
        score1 = v/freq_pairs[k[0], k[1]]
        rules_dict[rule1] = score1
        # x, z -> y
        rule2 = k[0] + " " + k[2] + " " + k[1]
        score2 = v/freq_pairs[k[0], k[2]]
        rules_dict[rule2] = score2
        # y, z -> x
        rule3 = k[1] + " " + k[2] + " " + k[0]
        score3 = v/freq_pairs[k[1], k[2]]
        rules_dict[rule3] = score3
    top5Rules = sorted(rules_dict.items(), key = lambda item:item[1], reverse=True) 
    return top5Rules[:5]

def print_result():
    baskets, total_entries = make_baskets()
    print("Total entries: ", total_entries)
    c_items = make_candidates(baskets)
    #print(c_items)
    freq_items = freq_itemsets(c_items)
    #print(freq_items)
    freqPair = freq_pairs(freq_items, baskets)
    print("Frequent pairs: ")
    print(*freqPair, sep = "\n")
    print("Number of frequent pairs: ",len(freqPair))
    conPairs = confidence_pairs(freqPair, freq_items)
    print("Top 5 pairs with highest confidence: ")
    print(*conPairs, sep = "\n")
    freqTriple = freq_triples(freq_items, baskets)
    print("Frequent triplets: ")
    print(*freqTriple, sep = "\n")
    print("Number of frequent triplets: ",len(freqTriple))
    conTrips = confidence_triples(freqTriple, freqPair)
    print("Top 5 pairs with highest confidence: ")
    print(*conTrips, sep = "\n")
    

start_time = time.time()
print_result()
print("--- %s seconds ---" % (time.time() - start_time))