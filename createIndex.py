import cPickle

def tokenize(fileObj):
	s = fileObj.read()
	return s.split()

def increaseFileSize(slabSize):
	fileObj = open("PostingList","ab+")
	retVal = fileObj.tell()
	for i in xrange(0,slabSize):
		fileObj.write('0')
	fileObj.close()
	return retVal

def buildIndexMapAndPosList(keyList, indexMap, slabSize, lastOffset, posList):
	i = 0
	# posList = {}
	for key in keyList:
		if not indexMap.has_key(key):
			indexMap[key] = lastOffset
			lastOffset += slabSize
			
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

def mergePostingList(postingListForABatch, indexMap, slabSize, bookKeeping, lastDump):
	fileObj = open("PostingList", "r+b")
	for key in postingListForABatch:	
		if lastDump.has_key(key): 
			fileObj.seek(lastDump[key], 0)
			try:
				fileContent = fileObj.read(slabSize).split('$')
				postingListForAWord = cPickle.loads(fileContent[2])
				postingListForAWord += postingListForABatch[key]
				dumpString = cPickle.dumps(postingListForAWord)
				if len(dumpString) + bookKeeping  < slabSize:
					fileObj.seek(lastDump[key], 0)
					fileObj.write(str(-1) + "$" + str(len(dumpString)) + "$")
					fileObj.seek(lastDump[key] + bookKeeping, 0)
					fileObj.write(dumpString)
				else:
					fileObj.seek(lastDump[key], 0)
					lastDump[key] = increaseFileSize(slabSize)
					fileObj.write(str(lastDump[key]) + "$" + fileContent[1] + "$")
					postingListForAWord = postingListForABatch[key]
					dumpString = cPickle.dumps(postingListForAWord)
					fileObj.seek(lastDump[key], 0)
					fileObj.write(str(-1) + "$" + str(len(dumpString)) + "$")
					fileObj.seek(lastDump[key] + bookKeeping, 0)
					fileObj.write(dumpString)
			except (EOFError,cPickle.UnpicklingError):
				continue
		else:
			lastDump[key] = indexMap[key]
			postingListForAWord = postingListForABatch[key]
			dumpString = cPickle.dumps(postingListForAWord)
			fileObj.seek(lastDump[key], 0)
			fileObj.write(str(-1) + "$" + str(len(dumpString)) + "$")
			fileObj.seek(lastDump[key] + bookKeeping, 0)
			fileObj.write(dumpString)

	fileObj.close()

def buildPostingListForABatch(postingListForABatch, postingListForAFile, docId):
	for key in postingListForAFile:
		if not postingListForABatch.has_key(key):
			postingListForABatch[key] = [[docId, postingListForAFile[key]]]
		else:
			postingListForABatch[key].append([docId, postingListForAFile[key]])

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
	bookKeeping = 50
	slabSize = 6000 + bookKeeping
	lastOffset = 0
	lastDump = {}
	postingListForABatch = {}
	for i in xrange(0, 2):
		postingListForAFile = {}
		for j in xrange(0, 50):
			fileObj = open("./dataset/" + str(i) + "/" + str(j+50*i), "rb")
			keyList = tokenize(fileObj)
			fileObj.close()
			postingListForAFile = {}
			lastOffset = buildIndexMapAndPosList(keyList, indexMap, slabSize, lastOffset, postingListForAFile)
			buildPostingListForABatch(postingListForABatch, postingListForAFile, j)
			print "|keyList| = " + str(len(keyList))
			print str(j+50*i) + "done"
		mergePostingList(postingListForABatch, indexMap, slabSize, bookKeeping, lastDump)
	# Dumping the index into a file
	dumpIndexMap(indexMap)

	# readPostingFile(indexMap)
