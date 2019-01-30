from util import *
from itertools import groupby
import math
import copy

def readParameter(parameterFileName):
	MIS_dict = dict()
	SDC = 0
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


def readData(dataFileName):
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
