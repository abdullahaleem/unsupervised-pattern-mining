from util import *
from msps import *
from itertools import groupby
import math
import copy



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


def getFrequent(database, items, s):
#Returns frequent items(and their count), with support >= s

	frequentItems = []
	frequentItemsCount = []

	for i in range(len(items)):
		sup = supportCount(database, items[i])
		if sup >= s:
			frequentItems.append(items[i])
			frequentItemsCount.append(sup)

	return frequentItems, frequentItemsCount


def makeFrequent(set1, set2, set1Count, set2Count, prefix, database, SDC):
# generates more frequent patterns using prefix and generated sets.
	
	newPatterns1 = []
	newPatterns2 = []

	sdcCheck1 = []
	sdcCheck2 = []

	for i in range(len(set1)):
		for j in range(len(prefix)):
			for k in range(len(prefix[j])):
				if abs(supportCount(database,set1[i]) - supportCount(database,prefix[j][k])) > SDC:
					sdcCheck1.append(i)
					break
			else:
				continue
			break

	for i in range(len(set2)):
		for j in range(len(prefix)):
			for k in range(len(prefix[j])):
				if abs(supportCount(database, set2[i]) - supportCount(database, prefix[j][k])) > SDC:
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


def combine(projetedDatabase, prefix, ikMIS, database, items, SDC):
# combine fucntions uses all three funtions to generate more combinations with ik

	set1, set2 = split(projetedDatabase, prefix)

	set1Freq, set1CountFreq = getFrequent(set1, items, ikMIS)
	set2Freq, set2CountFreq = getFrequent(set2, items, ikMIS)

	newPatterns1, newPatterns2, newPatterns1Count, newPatterns2Count = makeFrequent(set1Freq, set2Freq, set1CountFreq, set2CountFreq, prefix, database, SDC)

	return newPatterns1, newPatterns2, newPatterns1Count, newPatterns2Count


def rPrefixSpan(database, databaseLength, items, MIS, SDC, ik):
# returns all frequent sequences and their count that include ik.
	ikMIS = MIS[ik]*databaseLength
	database = myDelete(database, ikMIS)
	frequent, ignoreThis = getFrequent(database, items, ikMIS)
	frequent = makeList(frequent)
	
	count = []
	for i in range(len(frequent)):
		count.append(supportCount(database, frequent[i][0][0]))

	i = 0
	while i < len(frequent):
		
		projectedDatabase = projectDatabase(database, frequent[i])
		newPatterns1, newPatterns2, newPatterns1Count, newPatterns2Count = combine(projectedDatabase, frequent[i], ikMIS, database, items, SDC)
		
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