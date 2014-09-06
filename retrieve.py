import cPickle
import sys
import createIndex

def getPostingList(initialOffset):
	fileObj = open(createIndex.postingListFile,"rb")
	nextOffest = initialOffset
	postingListForTerm = []
	while nextOffest!=-1:
		fileObj.seek(nextOffest,0)
		book = fileObj.read(createIndex.bookKeeping)
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

if __name__ == "__main__":
	query = str(sys.argv[1])
	indexMap = createIndex.readIndexMap()
	postingListForTerm = []
	if not indexMap.has_key(query):
		print "No relevant docs found"
	else:
		# print indexMap[query]
		offset = indexMap[query][0]
		postingListForTerm = getPostingList(offset)
	print postingListForTerm

	postingListTuple = []
	for node in postingListForTerm:
		tempTuple = (node[0],len(node[1]))
		postingListTuple.append(tempTuple)
	print postingListTuple

	print sorted(postingListTuple,key=lambda x: x[1])[::-1]
