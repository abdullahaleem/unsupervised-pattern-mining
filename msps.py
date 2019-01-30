from util import *
from readwrite import *
from rprefixspan import *



def msPrefixSpan(dataFile, parameterFile, outputFile):

	database = readData(dataFile) # reading input files and defining initial parameters
	databaseLength = len(database)
	MIS, SDC = readParameter(parameterFile)
	items = list(MIS.keys())
	SDC = SDC * databaseLength

	frequentSeq = []
	frequentSeqCount = []
	frequentItems = getFrequentItems(database, items, MIS) # Get the frequent Items from Database
	frequentItems = mySort(frequentItems, MIS) # Sort the frequent items

	for i in range(len(frequentItems)):    
	   
		databaseSelected = selectSequence(database, databaseLength, frequentItems[i], SDC)  # Get the Modified Database, Including ik and removing everthing not meeting misIk 
		freqItems, freqItemsCount = rPrefixSpan(databaseSelected, databaseLength, items, MIS,  SDC, frequentItems[i]) # runs the prefix span, returing frequent items and their count
		myRemove(database,frequentItems[i]) # removes ik from the database permenantly
		
		for j in range(len(freqItems)): # add the frequent items with ik to final list
			frequentSeq.append(freqItems[j])
			frequentSeqCount.append(freqItemsCount[j])
		

	writeOutput(frequentSeq, frequentSeqCount, outputFile)
	print("All patterns saved to", outputFile)
	
	return list(zip(*[frequentSeq, [x*(100/databaseLength) for x in frequentSeqCount]]))



def msPrefixSpanFor(dataFile, parameterFile, prefix):

	database = readData(dataFile) # reading input files and defining initial parameters
	databaseLength = len(database)
	MIS, SDC = readParameter(parameterFile)
	items = list(MIS.keys())
	SDC = SDC * databaseLength

	frequentSeq = []
	frequentSeqCount = []
	frequentItems = getFrequentItems(database, items, MIS) # Get the frequent Items from Database
	frequentItems = mySort(frequentItems, MIS) # Sort the frequent items

	for i in range(len(frequentItems)):    
	   
		databaseSelected = selectSequence(database, databaseLength, frequentItems[i], SDC)  # Get the Modified Database, Including ik and removing everthing not meeting misIk 
		freqItems, freqItemsCount = rPrefixSpan(databaseSelected, databaseLength, items, MIS,  SDC, frequentItems[i]) # runs the prefix span, returing frequent items and their count
		myRemove(database,frequentItems[i]) # removes ik from the database permenantly
		
		for j in range(len(freqItems)): # add the frequent items with ik to final list
			frequentSeq.append(freqItems[j])
			frequentSeqCount.append(freqItemsCount[j])
		
	
	# getting all seq containing the item
	freqIndex = []
	for i in range(len(frequentSeq)):
		temp = []
		startPoint = 0
		for j in range(len(prefix)):
			for k in range(startPoint,len(frequentSeq[i])):
				if set(prefix[j]) < set(frequentSeq[i][k]):
					temp.append(True)
					startPoint = k+1
					break
		if len(temp) == len(prefix):
			freqIndex.append(i)
	
	frequentSeqNew = [frequentSeq[x] for x in freqIndex]
	frequentSeqCountNew = [frequentSeqCount[x] for x in freqIndex]

	temp = list(zip(*[frequentSeqNew, [x*(100/databaseLength) for x in frequentSeqCountNew]]))
	temp1 = sorted(temp, key=lambda x: x[1], reverse=True)
	return temp1