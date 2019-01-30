from itertools import groupby
from msps import *
import math
import copy


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


def mySort(items, MIS):
# Sorts items according to their MIS values.

	temp = [[],[]]
	for item in items:
		temp[0].append(item)
		temp[1].append(MIS[item])

	temp1 = list(zip(*temp))
	temp1 = sorted(temp1, key=lambda x: x[1])
	temp2 = list(zip(*temp1))
	temp3 = list(temp2[0])
	return temp3


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


def getFrequentItems(database, items, MIS):
# Finds every item i whose count in the database is at least MIS(i)
	
	frequentItems=[]
	for i in range(len(items)):
		sup = supportCount(database,items[i])
		mis = MIS[items[i]]
		
		if sup >= mis*len(database):
			frequentItems.append(items[i])
		
	return frequentItems


def selectSequence(database, databaseLength, item, phi):

	candidateSeq = []
	origPhi = phi

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


