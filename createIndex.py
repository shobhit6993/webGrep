import cPickle

def tokenize(fileObj):
	s = fileObj.read()
	return s.split()

def increaseFileSize(slabSize):
	fileObj = open("PostingList","ab+")
	for i in xrange(0,slabSize):
		fileObj.write('0')
	fileObj.close()

def buildIndexMapAndPosList(keyList, indexMap, slabSize, lastOffset, posList):
	i = 0
	# posList = {}
	for key in keyList:
		if not indexMap.has_key(key):
			indexMap[key] = lastOffset
			lastOffset += slabSize
			increaseFileSize(slabSize)

		if not posList.has_key(key):
			posList[keyList[i]] = [i]
		else:
			posList[keyList[i]].append(i)

		i += 1
	# print posList
	return lastOffset

def dumpIndexMap(indexMap):
	cPickle.dump(indexMap, open("OffsetMap", "wb"))

def readIndexMap():
	return cPickle.load(open("OffsetMap", "rb"))

def mergePostingList(postingListForAFile, indexMap, docId, slabSize, dumpedOnce):
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
	slabSize = 10000
	lastOffset = 0
	dumpedOnce = {}
	for i in xrange(0, 1):
		postingListForAFile = {}
		for j in xrange(0, 101):
			fileObj = open("./" + str(i) + "/" + str(j), "rb")
			keyList = tokenize(fileObj)
			fileObj.close()
			postingListForAFile = {}
			lastOffset = buildIndexMapAndPosList(keyList, indexMap, slabSize, lastOffset, postingListForAFile)
			mergePostingList(postingListForAFile, indexMap, j, slabSize, dumpedOnce)
			
			print "|keyList| = " + str(len(keyList))
			print str(j) + "done"
	
	# Dumping the index into a file
	dumpIndexMap(indexMap)

	# readPostingFile(indexMap)
