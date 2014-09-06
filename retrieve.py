import cPickle
import sys
from createIndex import postingListFile, bookKeeping, readIndexMap

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
	for node in postingListForTerm:
		tempTuple = (node[0],len(node[1]))
		postingListTuple.append(tempTuple)
	return postingListTuple

def intersectionOfTupleList(list1, list2):
	if len(list1) < len(list2):
		list1, list2 = list2, list1

	print list1
	print list2

	mergedList = []
	i = 0
	j = 0
	while (j != len(list2)):
		print str(i) + " " + str(j)
		if list1[i][0] == list2[j][0]:
			mergedList.append((list1[i][0], min(list1[i][1], list2[j][1])))
			i += 1
			j += 1
		elif list1[i][0] < list2[j][0]:
			i += 1
		else:
			j += 1

	return mergedList

def unionOfTupleList(list1, list2):
	if len(list1) < len(list2):
		list1, list2 = list2, list1

	mergedList = []
	i = 0
	j = 0
	while (i != len(list1)):
		if j == len(list2):
			mergedList.append(list1[i])
			i += 1
		elif list1[i][0] == list2[j][0]:
			mergedList.append((list1[i][0], list1[i][1] + list2[j][1]))
			i += 1
			j += 1
		elif list1[i][0] < list2[j][0]:
			mergedList.append(list1[i])
			i += 1
		else:
			mergedList.append(list2[j])
			j += 1

	return mergedList

if __name__ == "__main__":
	query = str(sys.argv[1])
	indexMap = readIndexMap()
	postingListForTerm = []
	if not indexMap.has_key(query):
		print "No relevant docs found"
	else:
		# print indexMap[query]
		offset = indexMap[query][0]
		postingListForTerm = getPostingList(offset)
	print postingListForTerm

	postingListTuple = convertToTuple(postingListForTerm)
	

	print sorted(postingListTuple,key=lambda x: x[1])[::-1]
