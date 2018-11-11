from itertools import groupby
import math
import copy


#____READ-WRITE___________________________________________________________________________________________________________________________


def read_parameter_file(parameterFileName):
    MIS_dict = dict()
    with open(parameterFileName) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for paramLine in content[:-1]:
        item_pos = paramLine.strip().find(")")
        if item_pos != -1:
            item = paramLine[4:item_pos]
            value_pos = paramLine.find("= ")
            if value_pos != -1:
                value = paramLine[value_pos+2:].strip()
                MIS_dict[item] = float(value)
    SDC_line = content[-1]
    SDCval_pos = SDC_line.find("= ")
    if SDCval_pos != -1:
        SDC = SDC_line[SDCval_pos + 2:].strip()

    return MIS_dict, float(SDC)


def read_data_file(dataFileName):
    all_lists = []
    with open(dataFileName) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for dataLine in content:
        all_lists.append(extract_sets_from_string(dataLine))
    return all_lists


def get_list_from_set_string(set_string):
    out = []
    items_begin = set_string.find("{")
    items_end = set_string.find("}")
    itemStr = set_string[items_begin+1:items_end]
    out = itemStr.split(",")
    return [x.strip() for x in out]


def extract_sets_from_string(string):
    list_of_sets = []
    string = string.strip()
    open_braces = list(find_all(string, "{"))
    close_braces = list(find_all(string, "}"))
    for i in range(0, len(open_braces)):
        curr_set = string[open_braces[i]:close_braces[i]+1]
        list_of_sets.append(get_list_from_set_string(curr_set))
    return list_of_sets


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


def get_seq_len(item):
    if type(item) == list:
        return sum(get_seq_len(subitem) for subitem in item)
    else:
        return 1


def get_writable_seq_string(seq):
    resultStr = "<"
    for itemSet in seq:
        resultStr = resultStr + "{"
        for item in itemSet:
            resultStr = resultStr + item + " "
        resultStr = resultStr + "}"
    resultStr = resultStr + ">"
    return resultStr


def writeOutput(sequenceList, CountList, fileName):

    seqLens = []
    for seq in sequenceList:
        seqLen = get_seq_len(seq)
        seqLens.append(seqLen)

    writeDic = dict()
    for key, group in groupby(seqLens):
        writeDic[key] = []

    for seq in sequenceList:
        writeDic[get_seq_len(seq)].append([seq, CountList[sequenceList.index(seq)]])

    with open(fileName, 'w+') as result_file:

        for key in writeDic:
            result_file.write("The number of length " + str(key) + " sequential patterns is " + str(len(writeDic[key]))+"\n")
            for seq, count in writeDic[key]:
                result_file.write("Pattern : " + get_writable_seq_string(seq)+":Count="+str(count)+"\n")



                
#____HELPERS______________________________________________________________________________________________________________________________   
        
            
def supportCount(database, item):
# returns the support count of an item in the database

    count = 0;
    for sequence in database:
        for itemset in sequence:
            for itemsetItem in itemset:
                if itemsetItem == item:
                    count = count + 1
                    break
            if itemsetItem == item:
                break
    return count


def makeList(data):
# coverts a list of items into a list of list of item.
    newList = []
    for item in data:
        newList.append([[item]])
    return newList


def mySort(items):
# Sorts items according to their MIS values.

    temp = [[],[]]
    for item in items:
        temp[0].append(item)
        temp[1].append(MIS[item])

    temp = zip(*temp)
    temp.sort(key=lambda x: x[1])
    temp = zip(*temp)
    return temp[0]


def myRemove(database, item):
# removes an item from the database permenantly

    i = 0
    a = len(database)
    while i < a:
        j = 0
        b = len(database[i])
        while j < b:
            k = 0
            c = len(database[i][j])
            while k < c:
                if database[i][j][k] == item:
                    del database[i][j][k]
                    k -= 1
                    c -= 1
                    # removing empty lists
                    if len(database[i][j])==0:
                        del database[i][j]
                        j -= 1
                        b -= 1
                k += 1
            j += 1
        i += 1   


def mySelect(database, databaseCount, item):
# Removes everything from database not containing item, parallely from count database too.

    databaseNew = []
    databaseCountNew = []

    for i in range(len(database)):
        for j in range(len(database[i])):
            if item in database[i][j]:
                databaseNew.append(database[i])
                databaseCountNew.append(databaseCount[i])
                break

    return databaseNew, databaseCountNew


def getFrequentItems(database):
# Finds every item i whose count in the database is at least MIS(i)

    frequentItems=[]
    for i in range(len(items)):
        sup = supportCount(database,items[i])
        mis = MIS[items[i]]
        
        if sup >= mis*len(database):
            frequentItems.append(items[i])
        
    return frequentItems


def selectSequence(database, item, phi):

    candidateSeq = []
    origPhi = phi
    phi = phi*databaseLength

    for i in range(len(database)):
        for j in range(len(database[i])):
            if item in database[i][j]:
                candidateSeq.append(database[i])
                break

    remove = []
    for seq in candidateSeq:
        for itemSetJ in seq:
            for itemJ in itemSetJ:
                sc_ik = supportCount(database, item)
                sc_ij = supportCount(database, itemJ)
                if itemJ != item and abs(sc_ik - sc_ij) > phi and itemJ not in remove:
                    remove.append(itemJ)

    candidateSeq_Copy = copy.deepcopy(candidateSeq)

    for seq in candidateSeq_Copy[:]:
        for itemSetJ in seq[:]:
            for itemJ in itemSetJ[:]:
                if itemJ in remove:
                    if len(itemSetJ) == 1:
                        if len(seq) == 1:
                            candidateSeq_Copy.remove(seq)
                        else:
                            seq.remove(itemSetJ)
                    else:
                        itemSetJ.remove(itemJ)

    return candidateSeq_Copy


def projectDatabase(databaseOrig,prefix):
# Gives a projected DB for a prefix f
    
    database = copy.deepcopy(databaseOrig)          # dont want to change the orignal database
    
    # getting all seq containing the prefix
    freqIndex = []
    for i in range(len(database)):
        temp = []
        startPoint = 0
        for j in range(len(prefix)):
            for k in range(startPoint,len(database[i])):
                if set(prefix[j]) <= set(database[i][k]):
                    temp.append(True)
                    startPoint = k+1
                    break
        if len(temp) == len(prefix):
            freqIndex.append(i)
    
    databaseModified = [database[x] for x in freqIndex]


    # Suffix extraction
    startPoint = 0
    lastElement = prefix[-1][-1]
    
    for i in range(len(databaseModified)):
        startPoint = 0
        for j in range(len(prefix)):
            for k in range(startPoint,len(databaseModified[i])):
                if set(prefix[j]) <= set(databaseModified[i][k]):
                    startPoint = k+1
                    break
        startPoint -= 1
            
        for j in range(len(databaseModified[i][startPoint])):
            if databaseModified[i][startPoint][j] == lastElement:
                if j == (len(databaseModified[i][startPoint])-1):
                    del databaseModified[i][0:startPoint+1]
                elif j == 0:
                    databaseModified[i][startPoint][j] = "_"
                    del databaseModified[i][0:startPoint]  
                else:
                    databaseModified[i][startPoint][j] = "_"
                    del databaseModified[i][startPoint][0:j]
                    del databaseModified[i][0:startPoint]
                break

    databaseModified = [x for x in databaseModified if x != []]
    return databaseModified



#____R-PREFIXSPAN_________________________________________________________________________________________________________________________


def myDelete(databaseOrig, s):
# deleting everything that has support less than s. Returns altered copy. Keeps orignal same.

    database = copy.deepcopy(databaseOrig)
    i = 0
    a = len(database)
    while i < a:
        j = 0
        b = len(database[i])
        while j < b:
            k = 0
            c = len(database[i][j])
            while k < c:
                if supportCount(database, database[i][j][k]) < s:
                    del database[i][j][k]
                    k -= 1
                    c -= 1

                    # removing empty lists
                    if len(database[i][j])==0:
                        del database[i][j]
                        j -= 1
                        b -= 1
                    if len(database[i])==0:
                        del database[i]
                        i -= 1
                        a -= 1
                k += 1
            j += 1
        i += 1
    return database


def split(databaseOrig, prefix):
# splits the database into the two possible combinations

    database = copy.deepcopy(databaseOrig)

    set1 = []       # will generate new sequence with new item in the same itemset
    set2 = []       # will generate new sequence with new item in a different itemset
    
    for seq in database:
        temp = []
        if seq[0][0] == '_':
            temp.append(seq[0])

        for i in range(0,len(seq)):
            if set(prefix[-1]) <= set(seq[i]):
                for j in range(len(seq[i])):
                    if seq[i][j] == prefix[-1][-1]:
                        if j == (len(seq[i])-1):
                            credits = 'written and directed by Abdullah Aleem, also, ignore this if condition'
                        elif j == 0:
                            seq[i][j] = "_"
                            temp.append(seq[i])
                        else:
                            seq[i][j] = "_"
                            del seq[i][0:j]
                            temp.append(seq[i])   
                        break
        set1.append(temp)
    
    database = copy.deepcopy(databaseOrig)
    for seq in database:
        if seq[0][0] == "_" and len(seq) > 1:
            set2.append(seq[1:])
        if seq[0][0] != "_":
            set2.append(seq)

    
    return set1, set2


def getFrequent(database, s):
#Returns frequent items(and their count), with support >= s

    frequentItems = []
    frequentItemsCount = []

    for i in range(len(items)):
        sup = supportCount(database, items[i])
        if sup >= s:
            frequentItems.append(items[i])
            frequentItemsCount.append(sup)

    return frequentItems, frequentItemsCount


def makeFrequent(set1, set2, set1Count, set2Count, prefix):
# generates more frequent patterns using prefix and generated sets.
    
    newPatterns1 = []
    newPatterns2 = []

    sdcCheck1 = []
    sdcCheck2 = []

    for i in range(len(set1)):
        for j in range(len(prefix)):
            for k in range(len(prefix[j])):
                if abs(supportCount(database,set1[i]) - supportCount(database,prefix[j][k])) > SDC*databaseLength:
                    sdcCheck1.append(i)
                    break
            else:
                continue
            break

    for i in range(len(set2)):
        for j in range(len(prefix)):
            for k in range(len(prefix[j])):
                if abs(supportCount(database, set2[i]) - supportCount(database, prefix[j][k])) > SDC*databaseLength:
                    sdcCheck2.append(i)
                    break
            else:
                continue
            break

    set1 = [i for j, i in enumerate(set1) if j not in sdcCheck1]
    set1Count = [i for j, i in enumerate(set1Count) if j not in sdcCheck1]

    set2 = [i for j, i in enumerate(set2) if j not in sdcCheck2]
    set2Count = [i for j, i in enumerate(set2Count) if j not in sdcCheck2]


    for i in range(len(set1)):
        alpha = copy.deepcopy(prefix)
        alpha[-1].append(set1[i])
        newPatterns1.append(alpha)

    for i in range(len(set2)):
        beta = copy.deepcopy(prefix)
        temp = [set2[i]]
        beta.append(temp)
        newPatterns2.append(beta)

    return newPatterns1, newPatterns2, set1Count, set2Count


def combine(projetedDatabase, prefix, ikMIS):
# combine fucntions uses all three funtions to generate more combinations with ik

    set1, set2 = split(projetedDatabase, prefix)

    set1Freq, set1CountFreq = getFrequent(set1, ikMIS)
    set2Freq, set2CountFreq = getFrequent(set2, ikMIS)

    newPatterns1, newPatterns2, newPatterns1Count, newPatterns2Count = makeFrequent(set1Freq, set2Freq, set1CountFreq, set2CountFreq, prefix)

    return newPatterns1, newPatterns2, newPatterns1Count, newPatterns2Count


def rPrefixSpan(database, ik):
# returns all frequent sequences and their count that include ik.
    ikMIS = MIS[ik]*databaseLength
    database = myDelete(database, ikMIS)
    frequent, ignoreThis = getFrequent(database, ikMIS)
    frequent = makeList(frequent)
    
    count = []
    for i in range(len(frequent)):
        count.append(supportCount(database, frequent[i][0][0]))

    i = 0
    while i < len(frequent):
        
        projectedDatabase = projectDatabase(database, frequent[i])
        newPatterns1, newPatterns2, newPatterns1Count, newPatterns2Count = combine(projectedDatabase, frequent[i], ikMIS)
        
        for alpha in range(len(newPatterns1)):
            frequent.append(newPatterns1[alpha])
            count.append(newPatterns1Count[alpha])

        for alpha in range(len(newPatterns2)):
            frequent.append(newPatterns2[alpha])
            count.append(newPatterns2Count[alpha])
            
        newPatterns1 = []
        newPatterns2 = []   

        i += 1

    frequent, count = mySelect(frequent, count, ik)

    return frequent, count



#____MAIN_________________________________________________________________________________________________________________________________


parameterFile = "parameters_100.txt"
dataFile = "data_100.txt"
outputFile = 'result_100.txt'

database = read_data_file(dataFile) # reading input files and defining initial parameters
databaseLength = len(database)
MIS, SDC = read_parameter_file(parameterFile)
items = (MIS.keys())

frequentSeq = []
frequentSeqCount = []
frequentItems = getFrequentItems(database) # Get the frequent Items from Database
frequentItems = mySort(frequentItems) # Sort the frequent items

for i in range(len(frequentItems)):    
   
    databaseSelected = selectSequence(database, frequentItems[i], SDC)  # Get the Modified Database, Including ik and removing everthing not meeting misIk 
    freqItems, freqItemsCount = rPrefixSpan(databaseSelected, frequentItems[i]) # runs the prefix span, returing frequent items and their count
    myRemove(database,frequentItems[i]) # removes ik from the database permenantly
    
    for j in range(len(freqItems)): # add the frequent items with ik to final list
        frequentSeq.append(freqItems[j])
        frequentSeqCount.append(freqItemsCount[j])
    
    print(str(i+1) +" by " + str(len(frequentItems)) + ' done!')
