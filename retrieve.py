import cPickle
import sys
from createIndex import postingListFile, bookKeeping, readIndexMap
import math

def getPostingList(initialOffset):
	fileObj = open(postingListFile,"rb")
	nextOffest = initialOffset
	postingListForTerm = []
	while nextOffest!=-1:
		fileObj.seek(nextOffest,0)
		book = fileObj.read(bookKeeping)
		# print book
		nextOffest = int(book.split('$')[0])
		# print nextOffest
		retrievedList = []
		try:
			retrievedList = cPickle.load(fileObj)
		except(EOFError,cPickle.UnpicklingError):
			print "error"

		# print retrievedList
		postingListForTerm += retrievedList
		# postingListForTerm.update(retrievedList)
	
	return postingListForTerm

def convertToTuple(postingListForTerm):
	postingListTuple = []
	for node in postingListForTerm:
		tempTuple = (node[0],len(node[1]))
		postingListTuple.append(tempTuple)
	return postingListTuple

def convertToTfIdfTuple(postingListForTerm, relevantDocs, totalDocs):
	postingListTuple = []
	idf = math.log(totalDocs / relevantDocs)
	for node in postingListForTerm:
		tempTuple = (node[0], round(len(node[1]) * idf,2))
		postingListTuple.append(tempTuple)
	return postingListTuple

def convertToBM25Tuple(postingListForTerm, relevantDocs, totalDocs, docLenList, avgDocLen):
	postingListTuple = []
	idf = math.log(totalDocs / relevantDocs)
	k = 1.6
	b = 0.75
	for node in postingListForTerm:
		tf = len(node[1])
		docLen = docLenList[node[0]]
		score = idf * ((tf * (k + 1))/(tf + k * (1 - b + b * (docLen / avgDocLen))))
		tempTuple = (node[0], score)
		postingListTuple.append(tempTuple)

	return postingListTuple



def intersectionOfTupleList(list1, list2, rankFunction):
	mergedList = []
	i = 0
	j = 0
	while i != len(list1) and j != len(list2):
		if list1[i][0] == list2[j][0]:
			mergedList.append((list1[i][0], rankFunction(list1[i][1], list2[j][1])))
			i += 1
			j += 1
		elif list1[i][0] > list2[j][0]:
			i += 1
		else:
			j += 1

	return mergedList

def unionOfTupleList(list1, list2):
	mergedList = []
	i = 0
	j = 0
	while i != len(list1) or j != len(list2):
		if j == len(list2):
			mergedList.append(list1[i])
			i += 1
		elif i == len(list1):
			mergedList.append(list2[j])
			j += 1
		elif list1[i][0] == list2[j][0]:
			mergedList.append((list1[i][0], list1[i][1] + list2[j][1]))
			i += 1
			j += 1
		elif list1[i][0] > list2[j][0]:
			mergedList.append(list1[i])
			i += 1
		else:
			mergedList.append(list2[j])
			j += 1
	
	return mergedList
	
def mergePhrasalLists(list1, list2):
	i = 0
	j = 0
	mergedList = []
	while i != len(list1) and j != len(list2):
		if list1[i][0] > list2[j][0]:
			i += 1
		elif list1[i][0] < list2[j][0]:
			j += 1
		else:
			tempList = [list1[i][0], []]
			flag = False
			k = 0
			l = 0
			while k != len(list1[i][1]) and l != len(list2[j][1]):
				if list1[i][1][k] + 1 < list2[j][1][l]:
					k += 1
				elif list1[i][1][k] + 1 > list2[j][1][l]:
					l += 1
				else:
					flag = True
					tempList[1].append(list2[j][1][l])
					k += 1
					l += 1
					
			if flag:
				mergedList.append(tempList)
			
			i += 1
			j += 1

	return mergedList	

if __name__ == "__main__":
	query = str(sys.argv[1])
	indexMap = readIndexMap()
	# postingListForTerm = []
	# if not indexMap.has_key(query):
	# 	print "No relevant docs found"
	# else:
	# 	# print indexMap[query]
	# 	offset = indexMap[query][0]
	# 	postingListForTerm = getPostingList(offset)
	# print postingListForTerm

	# postingListTuple = convertToTuple(postingListForTerm)
	# print postingListTuple

	# print sorted(postingListTuple,key=lambda x: x[1])[::-1]
