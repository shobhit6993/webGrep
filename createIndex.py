import cPickle

def tokenize(fileObj):
	s = fileObj.read()
	return s.split()

def increaseFileSize(slaSize):
	fileObj = open("PostingList","ab+")
	for i in xrange(0,slaSize):
		fileObj.write('0')
	fileObj.close()

def buildIndexMap(keyList, indexMap, slaSize, lastOffset):
	for key in keyList:
		if not indexMap.has_key(key):
			indexMap[key] = lastOffset
			lastOffset += slaSize
			increaseFileSize(slaSize)
	return lastOffset

def dumpIndexMap(indexMap):
	cPickle.dump(indexMap, open("OffsetMap", "wb"))

def readIndexMap():
	return cPickle.load(open("OffsetMap", "rb"))

def createPostingListForAFile(keyList, indexMap):
	posList = {}
	for i in xrange( 0, len(keyList) ):
		if posList.has_key(keyList[i]):
			posList[keyList[i]].append(i)
		else:
			posList[keyList[i]] = [i]
	return posList

def mergePostingList(postingListForAFile, indexMap, docId, slaSize, dumpedOnce):
	fileObj = open("PostingList", "r+b")
	for key in postingListForAFile:	
		if dumpedOnce.has_key(key): 
			fileObj.seek(indexMap[key], 0)
			try:
				postingListForAWord = cPickle.load(fileObj)
				postingListForAWord.append([docId, postingListForAFile[key]])
			except (EOFError,cPickle.UnpicklingError):
				continue
				
			
		else:
			dumpedOnce[key] = ""
			postingListForAWord = [[docId, postingListForAFile[key]]]
			
		fileObj.seek(indexMap[key], 0)
		tempDump = cPickle.dumps(postingListForAWord)
		fileObj.write(tempDump);
	fileObj.close()

def readPostingFile(indexMap):
	fileObj = open("PostingList", "rb")
	for key in indexMap:
		fileObj.seek(indexMap[key], 0)
		try:
			print cPickle.load(fileObj)
		except(EOFError,cPickle.UnpicklingError):
			continue
	
	fileObj.close()	
	

if __name__ == "__main__":
	fileObj = open("PostingList","wb")
	fileObj.close()
	# Tokenising the files to get a keyList
	keyList = []
	indexMap = {}
	slaSize = 10000
	lastOffset = 0
	dumpedOnce = {}
	for i in xrange(0, 1):
		for j in xrange(0, 101):
			fileObj = open("./" + str(i) + "/" + str(j), "rb")
			keyList = tokenize(fileObj)
			fileObj.close()
			lastOffset = buildIndexMap(keyList, indexMap, slaSize, lastOffset)
			postingListForAFile = createPostingListForAFile(keyList, indexMap)
			mergePostingList(postingListForAFile, indexMap, j, slaSize, dumpedOnce)
			print "|keyList| = " + str(len(keyList))
			print str(j) + "done"
	
	# Dumping the index into a file
	dumpIndexMap(indexMap)

	# readPostingFile(indexMap)
